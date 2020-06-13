"""Permet de générer toutes les configurations stables pour une taille donnée"""
from numpy import array, zeros, int64, copy, arange


def gen_line(possible, filled, n, i=0):
    """Generateur"""
    if not n:
        yield array(filled)
    else:
        for s in possible:
            filled[i] = s
            for el in gen_line(possible, filled, n - 1, i + 1):
                yield el


def gen_square(possible, filled, n, i=0):
    """Generateur"""
    if not n:
        yield array(filled)
    else:
        for s in possible:
            filled[i] = s
            for el in gen_line(possible, filled, n - 1, i + 1):
                yield el


def gen_all(nb_line):
    """Génénère un carré"""
    return gen_line(list(gen_line(
        range(0, 4), zeros(nb_line, dtype=int64), nb_line)),
        zeros((nb_line, nb_line), dtype=int64),
        nb_line)


if __name__ == '__main__':
    from time import perf_counter as perf
    # print(*gen_line([0, 1, 2, 3], [], 3), sep=2 * '\n')
    # print(len(list(gen_all(3))), sep=2 * '\n')
    # print(*gen_all(2), sep=2 * '\n')
    N = 400_000
    li = 4
    t = perf()
    for a, _ in zip(gen_all(li), range(N)):
        if a.any():
            pass
        else:
            pass
    dt = perf() - t
    print(f"Pour {N} configurations dt: {round(dt, 6)}\nPour toutes les {4 ** (li ** 2)} il faudrait {round((dt * 4 ** (li ** 2)) / N / 3600, 3)}h")

    # print(*c, sep=2 * '\n')
