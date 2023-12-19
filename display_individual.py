import pickle
import sys

from models.individual import Individual
from utils.sumo_utils import display

if __name__ == "__main__":
    print(sys.argv)
    if "--display-best" in sys.argv:
        with open('sumo/best_configuration.pkl', 'r') as f:
            indiv = pickle.load(f)
            phenotype = indiv.phenotype()
    else:
        indiv = Individual()
        phenotype = indiv.phenotype()

    display(phenotype)

    