import pickle
from pyeasyga import pyeasyga

from models.individual import Individual
from utils import hyperparams


def create_individual_fnc(data_):
    return Individual()


if __name__ == "__main__":
    initial_state = Individual()
    ga = pyeasyga.GeneticAlgorithm(None,
                                   population_size=hyperparams.POPULATION_SIZE,
                                   generations=hyperparams.GENERATIONS,
                                   crossover_probability=hyperparams.CROSSOVER_PROB,
                                   mutation_probability=hyperparams.MUTATION_PROB)

    fitnesses = []
    ga.create_individual = create_individual_fnc
    ga.crossover_function = Individual.crossover
    ga.mutate_function = Individual.mutate
    ga.fitness_function = lambda x, y: Individual.fitness(x, y, fitnesses) # to generate list of fitnesses

    ga.run()


    best = ga.best_individual()[1].phenotype()
    with open('results/best_configuration.pkl', 'wb') as f:
        pickle.dump(best, f)

    with open('results/fitnesses_list.pkl', 'wb') as f:
        pickle.dump(fitnesses, f)

    