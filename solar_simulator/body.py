from __future__ import annotations

import goopylib.imports as gp
import math
import os

from .vector import *


TRAIL_LENGTH = 100
SCALE = 1e9


class Body(gp.Renderable):
    instances: list[Body] = []

    draw_closest = True

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, graphic: str, trail_period: float):
        super().__init__()

        if os.path.isfile(graphic):
            self._renderable = gp.Image(graphic, (0, 0), 2 * radius, 2 * radius)
        else:
            self._renderable = gp.Circle((0, 0), radius)
            self._renderable.set_color(*self.get_color(graphic))

        self._renderable.z = 1

        self._pos = Vector2D(*pos)
        self._vel = Vector2D(*vel)
        self._pos_history = [self._pos]

        self._trail_period = trail_period
        self._last_trail_t = 0

        self._mass = mass
        self._radius = radius

        self._closest_line = gp.Line((0, 0), (0, 0))

        Body.instances.append(self)

        self._trail: list[gp.Circle] = [gp.Circle((0, 0), 1) for _ in range(TRAIL_LENGTH)]
        for i, point in enumerate(self._trail):
            point.set_color(gp.colors["whitesmoke"])
            point.set_transparency(i / TRAIL_LENGTH)

    def draw(self, window):
        for point in self._trail:
            point.draw(window)

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

        theta = math.atan2(*self._pos)
        self.rotation = math.degrees(theta) + 30

        for i in range(0, min(len(self._pos_history), TRAIL_LENGTH)):
            self._trail[i].position = tuple(self._pos_history[i] / SCALE)

        if self._closest_line.is_drawn():
            self._closest_line.destroy()

        if Body.draw_closest:
            if closest_body := self._find_closest_body():
                self._closest_line = gp.Line(self.position, closest_body.position, 2)
                self._closest_line.set_color(gp.colors["white"])
                self._closest_line.set_transparency(0.3)  # TODO renderable set_vertex_position methods
                self._closest_line.draw(self.window)

    def _find_closest_body(self):
        closest_dist = float("inf")
        closest_body = None

        for body in Body.instances:
            if isinstance(body, StationaryBody) or body == self:
                continue

            if (dist := math.dist(self.position, body.position)) < closest_dist:
                closest_dist = dist
                closest_body = body

        return closest_body

    @staticmethod
    def draw_all(window):
        for body in Body.instances:
            body.draw(window)

    @staticmethod
    def toggle_draw_closest(clicked):
        if not clicked:
            Body.draw_closest = not Body.draw_closest

    @staticmethod
    def update_all(frame):
        for body in Body.instances:
            body.update(frame)
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        if universe.T - self._last_trail_t > self._trail_period:
            self._pos_history.append(Vector2D(*value))
            self._last_trail_t = universe.T

            if len(self._pos_history) > TRAIL_LENGTH:
                self._pos_history.pop(0)

        self._pos = value

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, value):
        self._vel = value

    @property
    def mass(self):
        return self._mass


class StationaryBody(Body):
    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, graphic: str):
        super().__init__(pos=pos, vel=vel, mass=mass, radius=radius, graphic=graphic, trail_period=0)
        if isinstance(self._renderable, gp.Circle):
            self._renderable.set_color(graphic, gp.colors["white"], graphic, graphic)
        self._trail.clear()

    def update(self, frame):
        return


def rescale(mu):
    global SCALE
    SCALE = mu * 1.3e10 + (1 - mu) * 1e9


from . import engine as universe
