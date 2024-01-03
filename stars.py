import random

import numpy as np
import goopylib as gp


phases: np.array
periods: np.array
graphics: list[gp.Circle]

__frame = 100


def init(n, window):
    global phases, periods, graphics

    phases = np.pi * np.random.random(n)
    periods = (np.random.random(n) + 1) * np.pi / 75

    graphics = [gp.Circle((random.randint(-400, 400), random.randint(-400, 400)),
                          random.random()) for _ in range(n)]
    for star in graphics:
        star.set_color((random.randint(220, 255), random.randint(220, 255), random.randint(150, 255)))
        star.draw(window)

    twinkle()


def twinkle():
    global __frame
    __frame += 1

    alpha = (np.cos(phases + __frame * periods) + 1) / 5
    for i, star in enumerate(graphics):
        star.set_transparency(alpha[i])
