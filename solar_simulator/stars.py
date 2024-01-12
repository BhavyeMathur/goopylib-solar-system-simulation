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
        self.period = (2 * random.random() + 1) * (3.14159 / 100)

        self.graphic = gp.Circle((self.x, self.y), self.radius)
        self.graphic.draw(window)

        R = random.randint(220, 255)
        G = random.randint(180, 255)
        B = random.randint(150, G)
        self.graphic.set_color((R, G, B))

        self.twinkle()

    def twinkle(self):
        # TODO custom shader support (not for v2.0)
        self.graphic.transparency = (math.cos(self.phase + (mainloop.frame + 100) * self.period) + 1) / 4

    def move_to(self, x, y):
        self.graphic.position = (x + self.x, y + self.y)


stars: list[Star]


def init(n):
    global stars
    stars = [Star(mainloop.window) for _ in range(n)]


def twinkle():
    for star in stars:
        star.twinkle()


def wheel_overhead(x, y):
    for star in stars:
        star.move_to(x, y)
