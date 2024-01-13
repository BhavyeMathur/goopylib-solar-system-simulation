from __future__ import annotations

import goopylib.imports as gp
import math


from .vector import *


SCALE = 1e9


class Body(gp.Renderable):
    instances: list[Body] = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, graphic: None | str,
                 trail_period: float, follow_dt: float, follow_zoom: float):
        if graphic is None:
            self._renderable = gp.Circle((0, 0), radius)
        else:
            self._renderable = gp.Image(graphic, (0, 0), 2 * radius, 2 * radius)
            self._renderable.z = 1
        self.bounding_box = gp.Rectangle((0, 0), (50, 50))  # TODO add bounding boxes to goopylib

        self._pos = Vector2D(*pos)
        self.vel = Vector2D(*vel)

        self.mass = mass
        self.radius = radius

        self.follow_dt = follow_dt
        self.follow_zoom = follow_zoom

        self.closest_line = ClosestLine(self)

        self.trail = Trail(trail_period)
        self.trail.add_position(self._pos)

        self.id = len(Body.instances)
        Body.instances.append(self)

    def draw(self, window):
        self.trail.draw(window)
        self.closest_line.draw(window)

        if isinstance(self._renderable, gp.Image):
            super().draw(window)

    def update(self, frame):
        self.pos = Vector2D(*universe.positions[self.id])
        theta = math.atan2(*self._pos)

        self.position = tuple(self._pos / SCALE)
        self.rotation = math.degrees(theta)

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
        self.bounding_box.position = self.position
        return self.bounding_box.contains(x, y)


class StationaryBody(Body):
    instances: list[StationaryBody] = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, graphic: str = None):
        super().__init__(pos=pos, vel=vel, mass=mass, radius=radius, graphic=graphic,
                         trail_period=0, follow_dt=0, follow_zoom=0)
        self.trail.clear()
        StationaryBody.instances.append(self)

    def update(self, frame):
        self.position = tuple(self._pos / SCALE)


def init():
    for body in Body.instances:
        body.draw(mainloop.window)


def orbit():
    for body in Body.instances:
        body.update(mainloop.frame)


def rescale(mu):
    global SCALE
    SCALE = mu * 1.3e10 + (1 - mu) * 1e9


from . import mainloop
from .closest_planet import ClosestLine
from .trail import Trail
from . import engine as universe
