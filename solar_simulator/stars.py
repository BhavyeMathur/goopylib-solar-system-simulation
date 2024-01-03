import random

import math
import goopylib as gp

from . import mainloop


class Star:
    def __init__(self, window):
        self.x = random.randint(-400, 400)
        self.y = random.randint(-400, 400)

        color = (random.randint(220, 255), random.randint(220, 255), random.randint(150, 255))
        self.radius = random.random()

        self.phase = 3.14159 * random.random()
        self.period = (random.random() + 1) * (3.14159 / 75)

        self.graphic = gp.Circle((self.x, self.y), self.radius)
        self.graphic.set_color(color)
        self.graphic.draw(window)

        self.twinkle()

    def twinkle(self):
        self.graphic.set_transparency((math.cos(self.phase + mainloop.frame * self.period) + 1) / 5)


stars: list[Star]


def init(n, window):
    global stars
    stars = [Star(window) for _ in range(n)]


def twinkle():
    for star in stars:
        star.twinkle()
