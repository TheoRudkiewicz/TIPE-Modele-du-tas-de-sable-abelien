"""Permet de simuler l'éboulement d'un tas de sable sur un pavage triangulaire"""
# coding: utf-8
from time import perf_counter as perf
import numpy as np
from numba import jit
from svg_render import visualise


@jit(nopython=True)
def eboule(grid: np.array, li: int, col: int) -> None:
    """Eboule la case grid[li, col]
    Convention grid[li, col] conecté avec grid[li + 1, col] <=> li % 2 == col % 2"""
    nli, ncol = grid.shape
    nli -= 1
    ncol -= 1
    grid[li, col] -= 3  # on enlève
    # on va ajouter au voisins
    if li == 0:  # h
        if li % 2 == col % 2:  # connecté au dessous
            grid[li + 1, col] += 1

        if col == 0:  # g
            grid[li, col + 1] += 1
        elif col == ncol:
            grid[li, col - 1] += 1
        else:  # au milieu
            grid[li, col - 1] += 1
            grid[li, col + 1] += 1

    elif li == nli:  # b
        if li % 2 != col % 2:  # connecté au dessus
            grid[li - 1, col] += 1

        if col == 0:  # g
            grid[li, col + 1] += 1
        elif col == ncol:  # d
            grid[li, col - 1] += 1
        else:  # au milieu
            grid[li, col - 1] += 1
            grid[li, col + 1] += 1

    else:
        if li % 2 == col % 2:  # connecté au dessous
            grid[li + 1, col] += 1
        else:  # connecté au dessus
            grid[li - 1, col] += 1

        if col == 0:  # g
            grid[li, col + 1] += 1
        elif col == ncol:  # d
            grid[li, col - 1] += 1
        else:  # au milieu
            grid[li, col - 1] += 1
            grid[li, col + 1] += 1


@jit(nopython=True)
def stabilize(grid: np.array) -> None:
    nli, ncol = grid.shape
    while grid.max() >= 3:
        # print(grid.sum())
        for li in range(nli):
            for col in range(ncol):
                if grid[li, col] >= 3:
                    eboule(grid, li, col)


@jit(nopython=True)
def tas_transition_test(nb_line: int = 1, nb_column: int = 1) -> np.array:
    """Tas de test pour le critère de récurrence"""
    test = np.full((nb_line, nb_column), 0)
    test[0, :] += 1
    test[nb_line - 1, :] += 1
    test[:, 0] += 1
    test[:, nb_column - 1] += 1
    return test


@jit(nopython=True)
def neutral(nb_line: int = 1, nb_column: int = 1) -> np.array:
    """Renvoie le neutre, méthode algébrique"""
    e = np.full((nb_line, nb_column), 4)
    stabilize(e)
    e = np.full((nb_line, nb_column), 4) - e
    stabilize(e)
    return e


if __name__ == '__main__':
    t = perf()
    h = 300  # pair
    la = 251  # impair
    # d = 4
    # m = np.full((h, la), d)
    # stabilize(m)
    # im = visualise(m, name=f'{h}x{la}_{d}')
    # im.save(f'{h}x{la}_{d}')
    # im.show()

    m = neutral(h, la)
    im = visualise(m, name=f'{h}x{la}_e')
    print(f'{h}x{la}_e')
    
    print(perf() - t)


