"""La classe SandAutomate permet de manipuler
des tas de sable sur des grilles rectangulaires 2D n x m"""
from copy import deepcopy
import numpy as np
import tkinter as tk
from functools import partial


def aux_quit(window, _):
    window.quit()


class SandAutomate:
    def __init__(self, tas=None,  nb_line=10, nb_column=10, nb_start=0)-> None:
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
                return SandAutomate(self.tas + other.tas)
        elif isinstance(other, int):
            return SandAutomate(self.tas + other)
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
                return SandAutomate(self.tas - other.tas)
        elif isinstance(other, int):
            return SandAutomate(self.tas - other)
        else:
            raise TypeError(f'Other must be a SandAutomate, is {type(other)}')

    @property
    def full(self):
        """Return the full conf alias delta"""
        return SandAutomate(nb_line=self.nb_line, nb_column=self.nb_column, nb_start=3)

    @property
    def poids(self):
        """Donne le poid de la configuration"""
        return self.tas.sum()

    @property
    def tas_transition_test(self):
        test = np.full((self.nb_line, self.nb_column), 0)
        for col in range(self.nb_column):
            test[0][col] += 1
            test[self.nb_line - 1][col] += 1
        for line in range(self.nb_line):
            test[line][0] += 1
            test[line][self.nb_column - 1] += 1
        return SandAutomate(test)

    @property
    def neutral(self):
        """Renvoie le neutre, méthode Tangeante"""
        identity = SandAutomate(nb_line=self.nb_line, nb_column=self.nb_column)
        new_identity = identity + self.tas_transition_test
        new_identity.final_collapse()
        while new_identity != identity:
            identity = deepcopy(new_identity)
            new_identity = identity + self.tas_transition_test
            new_identity.final_collapse()
        return identity

    @property
    def neutral2(self):
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

    def show_grid(self, cnv)-> tk.Canvas:
        """Remplit le canvas"""
        dx = int(cnv['width']) / self.nb_line
        dy = int(cnv['height']) / self.nb_column
        for x in range(self.nb_line):
            for y in range(self.nb_column):
                if self.tas[x, y] == 0:
                    color = "white"
                elif self.tas[x, y] == 1:
                    color = "light gray"
                elif self.tas[x, y] == 2:
                    color = "dark gray"
                elif self.tas[x, y] == 3:
                    color = "gray"
                else:
                    color = "black"
                cnv.create_rectangle(
                    (y * dy, x * dx, (y + 1) * dy, (x + 1) * dx),
                    outline='', fill=color)
        return cnv

    def show(self)-> None:
        """Montre directement la config"""
        window = tk.Tk(className=f'Show a configuration')
        can = tk.Canvas(window, width=500, height=500)
        menu = tk.Menu(window)
        menu.add_command(label='Next Gen', command=window.quit)
        menu.add_command(label='End', command=window.destroy)
        nb = tk.Label(window,
                      text=f"Nombre de grains: {self.poids}")
        nb.pack()
        window.config(menu=menu)
        can.bind('<Button-1>', partial(aux_quit, window))
        self.show_grid(can).pack()
        window.mainloop()
        try:
            window.destroy()
        except tk.TclError:
            pass

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


if __name__ == '__main__':
    # SandAutomate(np.array([[0, 1, 2, 3, 4], [4, 3, 2, 1, 0], [0, 1, 2, 3, 4], [4, 3, 2, 1, 0]])).show()
    # help(SandAutomate)
    SandAutomate(nb_line=10, nb_column=10).tas_transition_test.show()
