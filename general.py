"""Différentes fonctions permettant de manipuler des tas de sable sous formes de tableau numpy
se voulant plus efficace que la classe en utilisant notamment la compilation avec numba"""

from numpy import array, full, arange
import numpy as np
from numba import jit
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def show(tas: array, title: str = '') -> None:
    color_map = ListedColormap(
        ['whitesmoke', 'red', 'indigo', 'blue', 'black', 'darkred', 'orange', 'yellow', 'darkblue'])
    im = plt.imshow(tas, cmap=color_map, vmin=-0.5, vmax=8.5)
    plt.subplots_adjust(bottom=0.01)
    plt.subplots_adjust(top=0.95)
    plt.subplots_adjust(left=0.01)
    plt.subplots_adjust(right=0.99)
    plt.colorbar(im, ticks=arange(0, 9))
    plt.axis('off')
    plt.title(title)
    plt.get_current_fig_manager().window.geometry("1900x1000+0+0")  # fenêtre en grand
    plt.show()


# @jit(nopython=True)
def random_grid_at_weight(nb_line: int, nb_column: int, p: int) -> array:
    """Génère une grille de poids donné"""
    grid = np.zeros((nb_line, nb_column), dtype=np.int64)
    nb_cases = nb_line * nb_column
    while p > 0:
        grid += np.bincount(np.random.randint(0, nb_cases, size=p), minlength=nb_cases).reshape((nb_line, nb_column))
        over = np.maximum(0, grid - 3)
        p = over.sum()
        grid -= over
    return grid


@jit(nopython=True)
def collapse_large(tas: array, li: int = 0, co: int = 0) -> int:
    """Eboule une case, avec un parcours en largeur"""
    nb_line, nb_column = tas.shape
    to_collapse_line = array([li])
    to_collapse_column = array([co])
    count_collapsed = 0
    nb = 1
    while nb:
        new_to_line = full(4 * nb + 4, -1)
        new_to_column = full(4 * nb + 4, -1)
        i = 0
        for line, column in zip(to_collapse_line, to_collapse_column):
            if tas[line][column] >= 4:
                tas[line][column] -= 4
                count_collapsed += 4
                if nb_line > line + 1 >= 0 and nb_column > column + 0 >= 0:
                    tas[line + 1, column + 0] += 1
                    if tas[line + 1, column + 0] >= 4:
                        new_to_line[4 * i] = line + 1
                        new_to_column[4 * i] = column
                if nb_line > line - 1 >= 0 and nb_column > column + 0 >= 0:
                    tas[line - 1, column + 0] += 1
                    if tas[line - 1, column + 0] >= 4:
                        new_to_line[4 * i + 1] = line - 1
                        new_to_column[4 * i + 1] = column
                if nb_line > line + 0 >= 0 and nb_column > column + 1 >= 0:
                    tas[line + 0, column + 1] += 1
                    if tas[line + 0, column + 1] >= 4:
                        new_to_line[4 * i + 2] = line
                        new_to_column[4 * i + 2] = column + 1
                if nb_line > line + 0 >= 0 and nb_column > column - 1 >= 0:
                    tas[line + 0, column - 1] += 1
                    if tas[line + 0, column - 1] >= 4:
                        new_to_line[4 * i + 3] = line
                        new_to_column[4 * i + 3] = column - 1
                i += 1
        to_collapse_line = new_to_line[new_to_line >= 0]
        to_collapse_column = new_to_column[new_to_column >= 0]
        nb = to_collapse_line.shape[0]
    return count_collapsed  # nombre de grain déplacer dans l'avalanche


@jit(nopython=True)
def self_collapse_large(tas: array, li: int = 0, co: int = 0) -> int:
    """Eboule une case, avec un parcours en largeur,
    autorise la case éboulé à contenir plus de 4 grains"""
    nb_line, nb_column = tas.shape
    to_collapse_line = array([li])
    to_collapse_column = array([co])
    count_collapsed = 0
    nb = 1
    while nb:
        new_to_line = full(5 * nb + 5, -1)
        new_to_column = full(5 * nb + 5, -1)
        i = 0
        for line, column in zip(to_collapse_line, to_collapse_column):
            if tas[line][column] >= 4:
                tas[line][column] -= 4
                count_collapsed += 4
                if tas[line, column] >= 4:
                    new_to_line[5 * i] = line
                    new_to_column[5 * i] = column
                if nb_line > line + 1 >= 0 and nb_column > column + 0 >= 0:
                    tas[line + 1, column + 0] += 1
                    if tas[line + 1, column + 0] >= 4:
                        new_to_line[5 * i + 1] = line + 1
                        new_to_column[5 * i + 1] = column
                if nb_line > line - 1 >= 0 and nb_column > column + 0 >= 0:
                    tas[line - 1, column + 0] += 1
                    if tas[line - 1, column + 0] >= 4:
                        new_to_line[5 * i + 2] = line - 1
                        new_to_column[5 * i + 2] = column
                if nb_line > line + 0 >= 0 and nb_column > column + 1 >= 0:
                    tas[line + 0, column + 1] += 1
                    if tas[line + 0, column + 1] >= 4:
                        new_to_line[5 * i + 3] = line
                        new_to_column[5 * i + 3] = column + 1
                if nb_line > line + 0 >= 0 and nb_column > column - 1 >= 0:
                    tas[line + 0, column - 1] += 1
                    if tas[line + 0, column - 1] >= 4:
                        new_to_line[5 * i + 4] = line
                        new_to_column[5 * i + 4] = column - 1
                i += 1
        to_collapse_line = new_to_line[new_to_line >= 0]
        to_collapse_column = new_to_column[new_to_column >= 0]
        nb = to_collapse_line.shape[0]
    return count_collapsed  # nombre de grain déplacer dans l'avalanche


@jit(nopython=True)
def collapse(tas: array, line: int = 0, column: int = 0, nb_line: int = 1, nb_column: int = 1) -> None:
    """Eboule une case, même si c'est illégal"""
    tas[line][column] -= 4
    if nb_line > line + 1 >= 0 and nb_column > column + 0 >= 0:
        tas[line + 1][column + 0] += 1
    if nb_line > line - 1 >= 0 and nb_column > column + 0 >= 0:
        tas[line - 1][column + 0] += 1
    if nb_line > line + 0 >= 0 and nb_column > column + 1 >= 0:
        tas[line + 0][column + 1] += 1
    if nb_line > line + 0 >= 0 and nb_column > column - 1 >= 0:
        tas[line + 0][column - 1] += 1


@jit(nopython=True)
def final_collapse(tas: array) -> int:
    """Eboule jusqu'à l'etat stable"""
    nb_line, nb_column = tas.shape
    count_collapsed = 0
    while tas.max() >= 4:
        for line in range(nb_line):
            for column in range(nb_column):
                if tas[line][column] >= 4:
                    count_collapsed += 4
                    collapse(tas, line, column, nb_line, nb_column)
    return count_collapsed  # nombre de grain déplacer dans l'avalanche


@jit(nopython=True)
def tas_transition_test(nb_line: int = 1, nb_column: int = 1) -> array:
    """Tas de test pour le critère de récurrence"""
    test = full((nb_line, nb_column), 0)
    test[0, :] += 1
    test[nb_line - 1, :] += 1
    test[:, 0] += 1
    test[:, nb_column - 1] += 1
    return test


@jit(nopython=True)
def neutral(nb_line: int = 1, nb_column: int = 1) -> array:
    """Renvoie le neutre, méthode algébrique"""
    e = full((nb_line, nb_column), 6)
    final_collapse(e)
    e = full((nb_line, nb_column), 6) - e
    final_collapse(e)
    return e


@jit(nopython=True)
def is_recurrent(tas: array, test: array) -> bool:
    """Renvoie True si tas est récurrent"""
    aux = tas + test
    final_collapse(aux)
    return (aux == tas).all()


if __name__ == '__main__':
    from time import perf_counter as perf
    # show(tas_transition_test(10, 10), title='Transition')
    g = 50_000
    n = int(g ** 0.5) + 1
    ex = full((n, n), 0)
    ex[n // 2, n // 2] += g
    t = perf()
    self_collapse_large(ex, n // 2, n // 2)
    print(perf() - t)
    show(ex, title=f'Eboulé de {g} du milieu sur {n}x{n}')

    # n = 51
    # ex = full((n, n), 3)
    # x, y = np.random.randint(0, n), np.random.randint(0, n)
    # x, y = 0, 0
    # ex[x, y] += 1
    # t = perf()
    # self_collapse_large(ex, x, y)
    # print(perf() - t)
    # show(ex, title=f'Eboulé de max instable par {x}, {y}')
    # ex[x, y] = 6
    # show(ex, title=f'Eboulé de max instable par {x}, {y}')

    # n = 501
    # show(neutral(n , n), title=f'Neutre {n},{n}')

    # n = 201
    # ex = full((n, n), 4)
    # t = perf()
    # final_collapse(ex)
    # print(perf() - t)
    # show(ex, title=f'Eboulé de max complé taille {n}')



