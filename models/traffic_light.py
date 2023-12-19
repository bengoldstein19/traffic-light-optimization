import random

class TrafficLight:
    # factual constants
    TRANSITION_TIME = 6
    MIN_ABSOLUTE_GREEN_TIME = 7
    MAX_ABSOLUTE_GREEN_TIME = 120

    # programming constants
    PHASE_DURATION_IDX = 0
    PHASE_STATE_IDX = 1

    def __init__(self, id: str, state_list: list, offset_time = None, green_time_list = None, cycle_time = None):
        self._state_list = state_list
        self._light_id = id

        self._num_stable_states = sum(TrafficLight.is_stable_state(s) for s in self._state_list)
        self._num_transition_states = len(self._state_list) - self._num_stable_states

        if offset_time is None:
            self._offset_time = random.random()
        else:
            self._offset_time = offset_time
        if green_time_list is None:
            self._green_time_list = [random.random() for _ in range(self._num_stable_states)]
        else:
            self._green_time_list = green_time_list
        if cycle_time is None:
            min_cycle_time = self._num_stable_states * TrafficLight.MIN_ABSOLUTE_GREEN_TIME + self._num_transition_states * TrafficLight.TRANSITION_TIME
            max_cycle_time = self._num_stable_states * TrafficLight.MAX_ABSOLUTE_GREEN_TIME + self._num_transition_states * TrafficLight.TRANSITION_TIME
            self._cycle_time = random.randint(min_cycle_time, max_cycle_time)
        else:
            self._cycle_time = cycle_time

    @classmethod
    def crossoverLights(cls, light1, light2, thresh: float):
        offset_rand = random.random()
        offset_time = light1.getOffsetTime() if offset_rand > thresh else light2.getOffsetTime()

        cycle_time_rand = random.random()
        cycle_time = light1.getCycleTime() if cycle_time_rand > thresh else light2.getCycleTime()

        green_times1 = light1.getGreenTimes()
        green_times2 = light2.getGreenTimes()

        green_times = [a if random.random() > thresh else b for a, b in zip(green_times1, green_times2)]

        return cls(light1.getLightId(), light1.getStateList(), offset_time, green_times, cycle_time)


    @staticmethod
    def addOffset(phenotype: list[tuple], offset_time: float):
        remaining_offset = offset_time
        while remaining_offset > 0:
            back_duration, back_state = phenotype[-1]
            if back_duration > remaining_offset:
                phenotype[-1] = (back_duration - remaining_offset, back_state)
                return [(remaining_offset, back_state)] + phenotype
            else:
                phenotype = [(back_duration, back_state)] + phenotype[:-1]
                remaining_offset -= back_duration
        return phenotype

    @staticmethod
    def is_stable_state(state: str):
        return 'y' in state.lower()

    def generatePhaseList(self) -> list[tuple]:
        adjusted_cycle_time = self._cycle_time - self._num_transition_states * TrafficLight.TRANSITION_TIME - self._num_stable_states * TrafficLight.MIN_ABSOLUTE_GREEN_TIME
        normalized_green_times = [green_time / sum(self._green_time_list) for green_time in self._green_time_list]
        stable_state_durations = [gt * adjusted_cycle_time + TrafficLight.MIN_ABSOLUTE_GREEN_TIME for gt in normalized_green_times]
        
        true_offset_time = self._offset_time * self._cycle_time

        stable_state_idx = 0
        no_offset_individual = []
        for state in self._state_list:
            if TrafficLight.is_stable_state(state):
                no_offset_individual.append((stable_state_durations[stable_state_idx], state))
                stable_state_idx += 1
            else:
                no_offset_individual.append((TrafficLight.TRANSITION_TIME, state))
        
        return TrafficLight.addOffset(no_offset_individual, true_offset_time)
    
    def getLightId(self) -> str:
        return self._light_id
    
    def getStateList(self) -> list[str]:
        return self._state_list
    
    def getCycleTime(self) -> float:
        return self._cycle_time
    
    def getOffsetTime(self) -> float:
        return self._offset_time
    
    def getGreenTimes(self) -> list:
        return self._green_time_list
    
    def mutate(self) -> list:
        attr_to_mutate = random.randint(0, 2)
        if attr_to_mutate == 0:
            min_cycle_time = self._num_stable_states * TrafficLight.MIN_ABSOLUTE_GREEN_TIME + self._num_transition_states * TrafficLight.TRANSITION_TIME
            max_cycle_time = self._num_stable_states * TrafficLight.MAX_ABSOLUTE_GREEN_TIME + self._num_transition_states * TrafficLight.TRANSITION_TIME
            self._cycle_time = random.randint(min_cycle_time, max_cycle_time)
        elif attr_to_mutate == 1:
            self._offset_time = random.random()
        else:
            self._green_time_list = [random.random() for _ in range(self._num_stable_states)]
            