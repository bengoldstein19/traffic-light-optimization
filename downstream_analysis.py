import matplotlib.pyplot as plt
import numpy as np
import pickle
from statistics import mean, stdev

GENERATIONS=25
POPULATION_SIZE=75


if __name__ == "__main__":
    with open('results/fitnesses_list.pkl', 'rb') as f:
        fitnesses = pickle.load(f)

    generation_fitnesses = []
    elite_fitnesses = []
    mean_fitnesses = []
    stdev_fitnesses = []

    print("BEST FIT", min(*fitnesses) / 171)

    for i in range(GENERATIONS):
        generation_fitnesses.append(fitnesses[POPULATION_SIZE*i:(POPULATION_SIZE)*(i+1)])

    for i in range(GENERATIONS):
        elite_fitnesses.append(min(generation_fitnesses[i]))
        mean_fitnesses.append(mean(generation_fitnesses[i]))
        stdev_fitnesses.append(stdev(generation_fitnesses[i]))
        
    print(elite_fitnesses)
    print(mean_fitnesses)
    print(stdev_fitnesses)

    fig, ax = plt.subplots()

    
    t = np.linspace(1, GENERATIONS, GENERATIONS * POPULATION_SIZE)
    p1 = ax.plot(t, fitnesses, label='Fitness')
    p2 = ax.plot(elite_fitnesses,'bs', label='Elite Fitness')
    p3 = ax.plot(mean_fitnesses, 'ro', label='Mean Fitness')

    ax2 = ax.twinx()
    p4 = ax2.plot(stdev_fitnesses, 'g*', label='Standard Deviation')
    ax2.set_ylabel('Variance')

    ax.set_xlabel('Generation')
    ax.set_ylabel('Penalty')
    lines = p1 + p2 + p3 + p4
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels)
    plt.show()