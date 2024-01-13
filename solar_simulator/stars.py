import random

import math
import goopylib as gp

from . import mainloop


class Star(gp.Circle):
    def __init__(self, window):
        self.xoffset = random.randint(-400, 400)
        self.yoffset = random.randint(-400, 400)

        self.radius = 1.1 * random.random()

        super().__init__((self.xoffset, self.yoffset), self.radius)
        self.draw(window)

        self.phase = 3.14159 * random.random()
        self.period = (2 * random.random() + 1) * (3.14159 / 50)

        R = random.randint(220, 255)
        G = random.randint(180, 255)
        B = random.randint(150, G)
        self.set_color((R, G, B))

        self.twinkle()

    def twinkle(self):
        # TODO custom shader support (not for v2.0)
        self.transparency = (math.cos(self.phase + (mainloop.frame + 100) * self.period) + 1) / 4

    @gp.Circle.position.setter
    def position(self, value):
        gp.Circle.position.fset(self, (value[0] + self.xoffset, value[1] + self.yoffset))


stars: list[Star]


def init(n):
    global stars
    stars = [Star(mainloop.window) for _ in range(n)]


def twinkle():
    for star in stars:
        star.twinkle()


def wheel_overhead(position):
    for star in stars:
        star.position = position
