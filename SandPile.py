"""Classe pour manipuler toutes les formes de tas de sable
définit par la matrice laplacienne. Cependant, c'est la classe de
Sagemath que j'ai utilisé"""
# coding: utf-8
import numpy as np


class SandPile:
    def __init__(self, c, delta):
        # assert
        self.delta = np.array(delta)
        self.c = np.array(c)
        self.delta_q = self.delta[1:, 1:]
        self.stable = abs(self.delta_q.diagonal())
        self.beta = self.delta[0, 1:]

    def __eq__(self, other):
        if isinstance(other, np.array):
            return (other == self.c).all()
        elif isinstance(other, SandPile):
            return (other.c == self.c).all()
        else:
            raise TypeError(f'other est un {type(other)}')

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.c)

    def __getitem__(self, item):
        return self.c[item]

    def __setitem__(self, key, value):
        self.c[key] = value

    def __and__(self, other):
        if isinstance(other, np.array):
            return SandPile(other + self.c, self.delta)
        elif isinstance(other, SandPile):
            return SandPile(other.c + self.c, self.delta)
        else:
            raise TypeError(f'other est un {type(other)}')

    def __iand__(self, other):
        return self & other

    def __rand__(self, other):
        return self & other

    def __add__(self, other):
        res = self & other
        res.stabilize()
        return res

    def __iadd__(self, other):
        return self + other

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return SandPile(-self.c, self.delta)

    def collapse(self, idx):
        self.c += self.delta_q[idx]

    def is_stable(self):
        return all(self.c < self.stable)

    def collapse_all(self):
        self.c += np.dot((self.c >= self.stable), self.delta_q)

    def stabilize(self):
        while not self.is_stable():
            self.collapse_all()

    @property
    def equivalent(self):
        """Renvoie le représentant récurrent de la configuration.
        Utilise l'algorithme thermique"""
        x0, x1 = self, self + self.beta
        while x0 != x1:
            x0, x1 = x1, x0 + self.beta
        return x0

    def are_equivalent(self, other) -> bool:
        return self.equivalent == other.equivalent

    @property
    def weight(self):
        return self.c.sum()

    @property
    def neutral(self):
        e = SandPile(2 * (self.stable - 1), self.delta)
        e.stabilize()
        e = -e + 2 * (self.stable - 1)
        e.stabilize()
        return e

    def is_recurrent(self):
        return self == self + self.beta

    def order(self):
        x0 = self
        omega = 0
        x = self + self
        while x0 != x:
            omega += 1
            x += self
        return omega

    @property
    def cardinality(self):
        return np.linalg.det(self.delta_q)





