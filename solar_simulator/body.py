from __future__ import annotations

import goopylib.imports as gp
import math


from .vector import *


SCALE = 1e9


class Body(gp.Renderable):
    instances: list[Body] = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, graphic: None | str,
                 trail_period: float, follow_dt: float, follow_zoom: float):
        super().__init__()

        if graphic is None:
            self._renderable = gp.Circle((0, 0), radius)
        else:
            self._renderable = gp.Image(graphic, (0, 0), 2 * radius, 2 * radius)
            self._renderable.z = 1
        self.bounding_box = gp.Rectangle((0, 0), (50, 50))  # TODO add bounding boxes

        self._pos = Vector2D(*pos)
        self.vel = Vector2D(*vel)

        self.mass = mass
        self.radius = radius

        self.follow_dt = follow_dt
        self.follow_zoom = follow_zoom

        self.closest_line = ClosestLine(self)

        self.trail = Trail(trail_period)
        self.trail.add_position(self._pos)

        Body.instances.append(self)

    def draw(self, window):
        self.trail.draw(window)
        self.closest_line.draw(window)

        if isinstance(self._renderable, gp.Image):
            super().draw(window)

    @staticmethod
    def get_color(color):
        shadow = gp.ColorHSV(*gp.hex_to_hsv(color))
        shadow.value = max(0.0, shadow.value - 0.3)
        shadow.saturation = min(1.0, shadow.saturation + 0.3)

        albedo = gp.ColorHSV(*gp.hex_to_hsv(color))
        albedo.value = min(1.0, 0.3 + albedo.value)
        albedo.saturation = max(0.0, albedo.saturation - 0.3)

        return color, albedo, shadow, gp.colors["black"]

    def update(self, frame):
        self.position = tuple(self._pos / SCALE)
        self.bounding_box.position = self.position

        theta = math.atan2(*self._pos)
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
        return self.bounding_box.contains(x, y)


class StationaryBody(Body):
    instances: list[StationaryBody] = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, graphic: str = None):
        super().__init__(pos=pos, vel=vel, mass=mass, radius=radius, graphic=None,
                         trail_period=0, follow_dt=0, follow_zoom=0)
        self.trail.clear()
        StationaryBody.instances.append(self)

    def update(self, frame):
        return


def init():
    for body in Body.instances:
        body.draw(mainloop.window)


def rescale(mu):
    global SCALE
    SCALE = mu * 1.3e10 + (1 - mu) * 1e9


def orbit():
    for body in Body.instances:
        body.update(mainloop.frame)


from . import mainloop
from .closest_planet import ClosestLine
from .trail import Trail
