from pyeasyga import pyeasyga
import pickle
from models.individual import Individual


def create_individual_fnc(data_):
    return Individual()


if __name__ == "__main__":
    initial_state = Individual()
    ga = pyeasyga.GeneticAlgorithm(None)
    ga.generations =  10
    ga.population_size = 20

    fitnesses = []
    
    
    ga.create_individual = create_individual_fnc
    ga.crossover_function = Individual.crossover
    ga.mutate_function = Individual.mutate
    ga.fitness_function = lambda x, y: Individual.fitness(x, y, fitnesses) # to generate list of fitnesses

    ga.run()


    best = ga.best_individual()[1].phenotype()
    with open('sumo/best_configuration.pkl', 'w') as f:
        pickle.dump(best, f)