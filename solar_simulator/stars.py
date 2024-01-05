import random

import math
import goopylib as gp

from . import mainloop


class Star:
    def __init__(self, window):
        self.x = random.randint(-400, 400)
        self.y = random.randint(-400, 400)

        self.radius = 1.1 * random.random()

        self.phase = 3.14159 * random.random()
        self.period = (2 * random.random() + 1) * (3.14159 / 75)

        self.graphic = gp.Circle((self.x, self.y), self.radius)
        self.graphic.draw(window)

        R = random.randint(220, 255)
        G = random.randint(180, 255)
        B = random.randint(150, G)
        self.graphic.set_color((R, G, B))

        self.twinkle()

    def twinkle(self):
        # TODO Custom shader support
        self.graphic.set_transparency((math.cos(self.phase + (mainloop.frame + 100) * self.period) + 1) / 4)


stars: list[Star]


def init(n, window):
    global stars
    stars = [Star(window) for _ in range(n)]


def twinkle():
    for star in stars:
        star.twinkle()
