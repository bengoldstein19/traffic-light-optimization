from sumolib import checkBinary
import traci

import sys
import xml.etree.ElementTree as ET

def simulate(program, input_cfg="sumo/simulation.sumocfg", output_tripinfo="sumo/simulation_tripinfo.xml"):
    traci.start([checkBinary(program), "-c", input_cfg, "--tripinfo-output", output_tripinfo, "--no-warnings"])
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
    traci.close()
    sys.stdout.flush()
    
    xmldoc = ET.parse(output_tripinfo)

    tripinfos = xmldoc.findall('tripinfo')

    waitingTime = 0
    for tripinfo in tripinfos:
        waitingTime += float(tripinfo.get('timeLoss'))
        if len(tripinfo.get('vaporized', "")) > 0:
            waitingTime += 2*float(tripinfo.get('timeLoss')) # 3x loss for teleporting
        
    return waitingTime

def display(phenotype):
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

    return simulate('sumo-gui')