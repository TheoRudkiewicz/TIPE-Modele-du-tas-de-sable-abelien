"""Permet de simuler le processus markovien et de récupérer des données issues de ce porcessus:
-la configuration avec le moins de grains de sable (poids min)
-le nombre d'apparition de chaque poids de configuration"""
# from Code.V2.general import *
from general import *
import numpy as np
from pickle import Pickler, Unpickler


def stats_from_markov(
        nb_line: int = 1,
        nb_column: int = 1,
        sample: int = 1_000)\
        -> tuple:
    """Génère des tas de sable stable aléatoirement.
    Revoie la liste de fréquences des tas récurents et non récurents"""
    min_array = None
    min_weight = nb_line * nb_column * 3
    weight_recurrent = np.zeros(nb_line * nb_column * 3 + 1, dtype=np.int64)
    collapse_weight = np.zeros(nb_line * nb_column * 18, dtype=np.int64)
    loosed_weight = np.zeros(nb_line * nb_column * 3 + 1, dtype=np.int64)

    tas = neutral(nb_line, nb_column)
    weight = tas.sum()
    old_weight = weight
    adding_location = 0, 0
    for _ in range(sample):
        while tas.max() <= 3:
            old_weight += 1
            adding_location = np.random.randint(0, nb_line), np.random.randint(0, nb_column)
            tas[adding_location] += 1

        this_collapse_weight = collapse_large(tas, adding_location[0], adding_location[1]) // 4

        weight = tas.sum()
        this_loosed_weight = old_weight - weight
        old_weight = weight

        # configuration
        weight_recurrent[weight] += 1
        if weight < min_weight:
            min_weight = weight
            min_array = np.copy(tas)

        # collapse weight
        if this_collapse_weight > nb_line * nb_column * 18:
            raise IndexError(f"{this_collapse_weight} est l'avalanche de trop")
        else:
            collapse_weight[this_collapse_weight] += 1

        # loosed weight
        loosed_weight[this_loosed_weight] += 1

    return nb_line, nb_column, sample, weight_recurrent, min_array, collapse_weight, loosed_weight


def save_stats(nb_line, nb_column, sample):
    """Save the stats"""
    with open(f"Data\Markov\\markov_{nb_line}_{nb_column}_{sample}", 'wb') as file:
        pic = Pickler(file)
        pic.dump(stats_from_markov(nb_line, nb_column, sample))


if __name__ == '__main__':
    from time import perf_counter as perf
    t = perf()
    save_stats(70, 70, 10_000_000)
    print(perf() - t)
