"""Permet de créé un svg représenatant une grille triangulaire"""
# coding: utf-8
import numpy as np
from PIL import Image, ImageDraw
from math import sqrt, ceil
import svgwrite


def visualise(grid: np.array, a: int = 10, name: str = 'error'):
    nl, nc = grid.shape
    # colors = ['white', 'blue', 'red', 'black', 'orange', 'yellow']
    colors = [svgwrite.rgb(255, 255, 255), svgwrite.rgb(0, 0, 255),
              svgwrite.rgb(255, 0, 0), svgwrite.rgb(255, 0, 0),
              svgwrite.rgb(255, 255, 0), svgwrite.rgb(0, 255, 0)]

    h = a * sqrt(3) / 2

    im = svgwrite.Drawing(f'{name}.svg', profile='full')

    for l in range(nl):
        if l % 2 == 1:
            for c in range(nc):
                if c % 2 == 0:
                    rcol = c // 2
                    im.add(svgwrite.shapes.Polygon(points=[(rcol * a, l * h),  # hg
                                  (rcol * a + a, l * h),  # hd
                                  (rcol * a + a // 2, l * h + h)  # bm
                                  ], fill=colors[grid[l, c]]))
                else:
                    rcol = c // 2
                    im.add(svgwrite.shapes.Polygon(points=[(rcol * a + 3 * a // 2, l * h + h),  # bd
                                  (rcol * a + a, l * h),  # hm
                                  (rcol * a + a // 2, l * h + h)  # bg
                                  ], fill=colors[grid[l, c]]))
        else:
            for c in range(nc):
                if c % 2 == 0:
                    rcol = c // 2
                    im.add(svgwrite.shapes.Polygon(points=[(rcol * a + a, l * h + h),  # bd
                                  (rcol * a + a // 2, l * h),  # hm
                                  (rcol * a, l * h + h)  # bg
                                  ], fill=colors[grid[l, c]]))
                else:
                    rcol = c // 2
                    im.add(svgwrite.shapes.Polygon(points=[(rcol * a + a // 2, l * h),  # hg
                                  (rcol * a + 3 * a // 2, l * h),  # hd
                                  (rcol * a + a, l * h + h)  # bm
                                  ], fill=colors[grid[l, c]]))
    im.save()


if __name__ == '__main__':
    p = 100
    ip = p + 1
    a = 10
    t = np.random.randint(5, size=(p, ip))
    i = visualise(t, a)
    print(t)
    help(svgwrite)



