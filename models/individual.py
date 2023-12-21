import random
import xml.etree.ElementTree as ET

from .traffic_light import TrafficLight
import sys
from utils.sumo_utils import simulate

class Individual:
    def __init__(self):
        self._id_to_light = {}
        self._signal_ids = Individual.getSignalIdsFromXML()
        id_to_states = Individual.getIdToStatesFromXML()
        for signal_id in self._signal_ids:
            self._id_to_light[signal_id] = TrafficLight(signal_id, id_to_states[signal_id])

    @classmethod
    def crossover(cls, parent1, parent2):
        child1 = cls()
        child2 = cls()
        for id in parent1.getSignalIds():
            parent1_light = parent1.getLightById(id)
            parent2_light = parent2.getLightById(id)
            thresh = random.random()
            child1_light = TrafficLight.crossoverLights(parent1_light, parent2_light, thresh)
            child2_light = TrafficLight.crossoverLights(parent2_light, parent1_light, thresh)
            child1.setLightById(id, child1_light)
            child2.setLightById(id, child2_light)

        return child1, child2
    
    @classmethod
    def mutate_light(cls, indiv):
        mutation_id = random.choice(indiv.getSignalIds())
        mutated_light = indiv.getLightById(mutation_id)
        mutated_light.mutate()
        
    @classmethod
    def mutate(cls, individual):
        Individual.mutate_light(individual)
        mutation_prevalence = random.random() * 0.9
        while random.random() < mutation_prevalence:
            Individual.mutate_light(individual)
        
    @staticmethod
    def getIdToStatesFromXML(xml_file='sumo/osm.net.xml') -> tuple[map]:
        states_by_id = {}
        network = ET.parse(xml_file)
        signals = network.findall('tlLogic')
        for signal in signals:
            signal_id = signal.get('id')
            states_by_id[signal_id] = []
            phases = signal.findall('phase')
            for phase in phases:
                states_by_id[signal_id].append(phase.get('state'))
        return states_by_id
    
    @staticmethod
    def getSignalIdsFromXML(xml_file='sumo/osm.net.xml') -> list:
        signal_ids = []
        network = ET.parse(xml_file)
        signals = network.findall('tlLogic')
        for signal in signals:
            signal_ids.append(signal.get('id'))
        return signal_ids
    
    def getSignalIds(self):
        return self._signal_ids
    
    def getStateById(self, id: str):
        return self._id_to_states[id]
    
    def setLightById(self, id: str, light: TrafficLight):
        self._id_to_light[id] = light

    def getLightById(self, id: str) -> TrafficLight:
        return self._id_to_light[id]
    
    def phenotype(self):
        phenotype = {}
        for id, light in self._id_to_light.items():
            phenotype[id] = light.generatePhaseList()

        return phenotype
    
    # data param to match pyeasyga format
    @classmethod
    def fitness(cls, individual, data, fitness_list: list):
        phenotype = individual.phenotype()

        network = ET.parse('sumo/osm.net.xml')
        signals = network.findall('tlLogic')
        
        for signal in signals:
            phases = signal.findall('phase')
            for p in phases:
                signal.remove(p)

            signal_id = signal.get('id')
            for dur, state in phenotype[signal_id]:
                new_phase = ET.Element('phase')
                new_phase.set('duration', str(dur))
                new_phase.set('state', state)
                signal.append(new_phase)

        network.write("sumo/simulation.net.xml")
        
        timeLoss = simulate('sumo')
        
        fitness_list.append(timeLoss)
            
        print(timeLoss, individual)
        
        return 1/timeLoss