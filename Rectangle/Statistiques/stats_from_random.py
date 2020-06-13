"""Permet de générer aléatoirement des configurations et de récupérer des données issues de ce processus:
la configuration avec le moins de grains de sable (poids min),
le nombre d'apparition de chaque poids de configuration."""
from general import *
import numpy as np
from pickle import Pickler


def stats_from_random(
        nb_line: int = 1,
        nb_column: int = 1,
        sample: int = 1_000,
        generator=lambda x, y: np.random.randint(0, 4, (x, y)))\
        -> tuple:
    """Génère des tas de sable stable aléatoirement.
    Revoie la liste de fréquences des tas récurents et non récurents"""
    max_array = None
    max_weight = 0
    min_array = None
    min_weight = nb_line * nb_column * 3
    test = tas_transition_test(nb_line, nb_column)
    weight_recurrent = np.zeros(nb_line * nb_column * 3 + 1, dtype=np.int64)
    weight_transient = np.zeros(nb_line * nb_column * 3 + 1, dtype=np.int64)
    for _ in range(sample):
        tas = generator(nb_line, nb_column)
        weight = tas.sum()
        if is_recurrent(tas, test):
            weight_recurrent[weight] += 1
            if weight < min_weight:
                min_weight = weight
                min_array = tas
        else:
            weight_transient[weight] += 1
            if weight > max_weight:
                max_weight = weight
                max_array = tas
    return nb_line, nb_column, sample, weight_transient, weight_recurrent, max_array, min_array


def save_stats(nb_line, nb_column, sample):
    """Save the stats"""
    with open(f"Data\Random\\random_{nb_line}_{nb_column}_{sample}", 'wb') as file:
        pic = Pickler(file)
        pic.dump(stats_from_random(nb_line, nb_column, sample))


if __name__ == '__main__':
    from time import perf_counter as perf
    t = perf()
    save_stats(5, 5, 10_000_000)
    print(perf() - t)
