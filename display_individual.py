import pickle
import sys

from models.individual import Individual
from utils.sumo_utils import display

if __name__ == "__main__":
    print(sys.argv)
    if "--best" in sys.argv:
        with open('results/best_configuration.pkl', 'rb') as f:
            phenotype = pickle.load(f)
    else:
        indiv = Individual()
        phenotype = indiv.phenotype()

    display(phenotype)

    