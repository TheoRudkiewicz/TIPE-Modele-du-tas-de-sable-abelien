"""La classe SandAutomate permet de manipuler des tas de sable sur des grilles rectangulaires"""
from copy import deepcopy
from functools import partial
import numpy as np

import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def aux_quit(window, _):
    window.quit()


class SandAutomate:
    def __init__(self, tas=None,  nb_line=10, nb_column=10, nb_start=0, show=False)-> None:
        self.show = show
        self.color_map = ListedColormap(
            ['white', 'lightblue', 'blue', 'darkblue', 'black', 'darkred', 'red', 'orange', 'yellow'])
        if tas is None:
            self.tas = np.full((nb_line, nb_column), nb_start)
            self.nb_line, self.nb_column = nb_line, nb_column
        else:
            self.tas = tas
            self.old_tas = None
            self.nb_line, self.nb_column = tas.shape

    def __str__(self):
        return str(self.tas)

    def __repr__(self):
        return str(self)

    def __eq__(self, other)-> bool:
        if isinstance(other, SandAutomate):
            if self.nb_line != other.nb_line:
                return False
            elif self.nb_column != other.nb_column:
                return False
            else:
                return (self.tas == other.tas).all()
        else:
            raise TypeError(f'Other must be a SandAutomate, is {type(other)}')

    def __ne__(self, other)-> bool:
        return not self == other

    def __add__(self, other):
        if isinstance(other, SandAutomate):
            if self.nb_line != other.nb_line:
                raise ValueError('Not the same number of line')
            elif self.nb_column != other.nb_column:
                raise ValueError('Not the same number of column')
            else:
                return SandAutomate(self.tas + other.tas, show=self.show)
        elif isinstance(other, int):
            return SandAutomate(self.tas + other, show=self.show)
        else:
            raise TypeError(f'Other must be a SandAutomate, is {type(other)}')

    def __iadd__(self, other):
        return self + other

    def __neg__(self):
        return SandAutomate(-self.tas)

    def __sub__(self, other):
        if isinstance(other, SandAutomate):
            if self.nb_line != other.nb_line:
                raise ValueError('Not the same number of line')
            elif self.nb_column != other.nb_column:
                raise ValueError('Not the same number of column')
            else:
                return SandAutomate(self.tas - other.tas, show=self.show)
        elif isinstance(other, int):
            return SandAutomate(self.tas - other, show=self.show)
        else:
            raise TypeError(f'Other must be a SandAutomate, is {type(other)}')

    @property
    def full(self):
        """Return the full conf alias delta"""
        return SandAutomate(nb_line=self.nb_line, nb_column=self.nb_column, nb_start=3, show=self.show)

    @property
    def poids(self):
        """Donne le poid de la configuration"""
        return self.tas.sum()

    @property
    def tas_transition_test(self):
        test = np.full((self.nb_line, self.nb_column), 0)
        test[0, :] += 1
        test[self.nb_line - 1, :] += 1
        test[:, 0] += 1
        test[:, self.nb_column - 1] += 1
        return SandAutomate(test, show=self.show)

    @property
    def neutral_algorithm(self):
        """Renvoie le neutre, méthode Tangeante"""
        identity = SandAutomate(nb_line=self.nb_line, nb_column=self.nb_column, nb_start=0, show=self.show)
        new_identity = identity + self.tas_transition_test
        new_identity.final_collapse()
        while new_identity != identity:
            identity = deepcopy(new_identity)
            new_identity = identity + self.tas_transition_test
            new_identity.final_collapse()
        return identity

    @property
    def neutral_algebra(self):
        """Renvoie le neutre, méthode générale"""
        e = self.full + self.full
        e.final_collapse()
        e = self.full + (self.full - e)
        e.final_collapse()
        return e

    def is_recurrent(self)-> bool:
        """Test si self est récurrent"""
        aux = self + self.tas_transition_test
        aux.final_collapse()
        return aux == self

    def is_stable(self)-> bool:
        """Renvoie True si la conf est stable"""
        return self.tas.max() < 4

    def add_grain(self):
        self.tas[np.random.randint(self.nb_line), np.random.randint(self.nb_column)] += 1

    def next_gen(self)-> None:
        """Passe à la génération suivante"""
        for line in range(self.nb_line):
            for column in range(self.nb_column):
                self.collapse(line, column)

    def collapse(self, line, column)-> None:
        """Eboule une case"""
        if self.tas[line][column] >= 4:
            self.tas[line][column] -= 4
            for dl, dc in (0, -1), (0, 1), (-1, 0), (1, 0):
                if self.nb_line > line + dl >= 0 and self.nb_column > column + dc >= 0:
                    self.tas[line + dl][column + dc] += 1

    def final_collapse(self)-> None:
        """Eboule jusqu'à l'etat stable"""
        while not self.is_stable():
            self.next_gen()
            if self.show:
                plt.clf()
                im = plt.imshow(self.tas, cmap=self.color_map, vmin=-0.5, vmax=8.5)
                plt.colorbar(im, ticks=np.arange(0, 9))
                plt.axis('off')
                plt.pause(0.00000000000001)

    def process(self, n):
        """Markov process"""
        for _ in range(n):
            self.add_grain()
            plt.clf()
            im = plt.imshow(self.tas, cmap=self.color_map, vmin=-0.5, vmax=8.5)
            plt.colorbar(im, ticks=np.arange(0, 9))
            plt.axis('off')
            plt.pause(0.0000000000000000001)
            if not self.is_stable():
                self.final_collapse()

    def showing(self)-> None:
        """Montre directement la config"""
        plt.clf()
        im = plt.imshow(self.tas, cmap=self.color_map, vmin=-0.5, vmax=8.5)
        plt.colorbar(im, ticks=np.arange(0, 9))
        plt.axis('off')
        plt.pause(2)

    def next_gen_synchrone(self)-> None:
        """Passe à la génération suivante"""
        self.old_tas = np.copy(self.tas)
        for line in range(self.nb_line):
            for column in range(self.nb_column):
                self.collapse_synchrone(line, column)

    def collapse_synchrone(self, line, column)-> None:
        """Eboule une case"""
        if self.old_tas[line][column] >= 4:
            self.tas[line][column] -= 4
            for dl, dc in (0, -1), (0, 1), (-1, 0), (1, 0):
                if self.nb_line > line + dl >= 0 and self.nb_column > column + dc >= 0:
                    self.tas[line + dl][column + dc] += 1

    def final_collapse_synchrone(self)-> None:
        """Eboule jusqu'à l'etat stable"""
        while not self.is_stable():
            self.next_gen_synchrone()
            self.next_gen_synchrone()
            self.next_gen_synchrone()
            self.next_gen_synchrone()
            if self.show:
                plt.clf()
                im = plt.imshow(self.tas, cmap=self.color_map, vmin=-0.5, vmax=8.5)
                plt.subplots_adjust(bottom=0.01)
                plt.subplots_adjust(top=0.99)
                plt.subplots_adjust(left=0.01)
                plt.subplots_adjust(right=0.99)
                plt.colorbar(im, ticks=np.arange(0, 9))
                plt.axis('off')
                plt.pause(0.00001)

    def neutral_algebra_sync(self):
        """Renvoie le neutre, méthode générale"""
        e = self.full + self.full
        e.final_collapse_synchrone()
        e = self.full + (self.full - e)
        e.final_collapse_synchrone()
        return e


if __name__ == '__main__':
    # SandAutomate(np.array([[0, 1, 2, 3, 4], [4, 3, 2, 1, 0], [0, 1, 2, 3, 4], [4, 3, 2, 1, 0]])).show()
    h = SandAutomate(nb_line=30, nb_column=30, nb_start=3, show=True)
    h.tas[8, 1] += 1
    h.final_collapse()
    # h.process(1_000_000)
    # # h.final_collapse()
    # h.showing()
    # # h.neutral_algebra_sync()

    plt.show()
    help(SandAutomate)
