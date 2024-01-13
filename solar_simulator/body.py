from __future__ import annotations

import goopylib.imports as gp
import math


SCALE = 1e9


class Body(gp.Renderable):
    instances: list[Body] = []

    def __init__(self, pos, vel, mass: float, radius: float, graphic: None | str = None,
                 trail_period: float = 0, follow_dt: float = 0, follow_zoom: float = 1):
        if graphic is None:
            self._renderable = gp.Circle((0, 0), radius)
        else:
            self._renderable = gp.Image(graphic, (0, 0), 2 * radius, 2 * radius)

        self.bounding_box = gp.Rectangle((-25, -25), (25, 25))  # TODO add bounding boxes to goopylib

        self.follow_dt = follow_dt
        self.follow_zoom = follow_zoom

        self.closest_line = ClosestLine(self)
        self.trail = Trail(trail_period)

        self.z = 1
        self.pos = pos
        self.vel = vel
        self.mass = mass

        Body.instances.append(self)

    def draw(self, window):
        self.trail.draw(window)
        self.closest_line.draw(window)

        if isinstance(self._renderable, gp.Image):
            super().draw(window)

    def update(self):
        self.position = tuple(self._pos / SCALE)
        self.rotation = 57.3 * math.atan2(*self.position)

        self.trail.update()
        self.closest_line.update()
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self.trail.add_position(value)
        self._pos = value

    def contains(self, x: float, y: float) -> bool:
        return self.bounding_box.contains(x - self.x, y - self.y)


class StationaryBody(Body):
    def update(self):
        return


def init():
    for body in Body.instances:
        body.draw(mainloop.window)


def orbit():
    for body in Body.instances:
        body.update()


def rescale(mu):
    global SCALE
    SCALE = mu * 1.3e10 + (1 - mu) * 1e9


from . import mainloop
from .closest_planet import ClosestLine
from .trail import Trail
