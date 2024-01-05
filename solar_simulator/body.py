import goopylib.imports as gp
import math

from .vector import *


TRAIL_LENGTH = 100
TRAIL_PERIOD = 20

SCALE = 1e9
LAST_SCALE = SCALE


class Body(gp.Renderable):
    instances = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, color: str):
        super().__init__()
        self._renderable = gp.Circle((0, 0), radius)
        self._renderable.set_color(*self.get_color(color))

        self._pos = Vector2D(*pos)
        self._vel = Vector2D(*vel)
        self._pos_history = [self._pos]

        self._mass = mass
        self._radius = radius

        Body.instances.append(self)

        self._trail: list[gp.Circle] = [gp.Circle((0, 0), 1) for _ in range(TRAIL_LENGTH)]
        for i, point in enumerate(self._trail):
            point.set_color(gp.colors["whitesmoke"])
            point.set_transparency(i / TRAIL_LENGTH)

    def draw(self, window):
        super().draw(window)

        for point in self._trail:
            point.draw(self.window)

    @staticmethod
    def get_color(color):
        shadow = gp.ColorHSV(*gp.hex_to_hsv(color))
        shadow.value -= 0.3
        shadow.saturation += 0.3

        albedo = gp.ColorHSV(*gp.hex_to_hsv(color))
        albedo.value = min(1.0, 0.3 + albedo.value)  # value should automatically be clamped, accept ints
        albedo.saturation -= 0.3

        return color, albedo, shadow, gp.colors["black"]

    def update(self, frame):
        self.x = self._pos.x / SCALE
        self.y = self._pos.y / SCALE

        theta = math.atan2(*self._pos)
        self.rotation = math.degrees(theta) + 30

        if len(self._pos_history) >= TRAIL_PERIOD * TRAIL_LENGTH:
            self._pos_history = self._pos_history[-(TRAIL_PERIOD * TRAIL_LENGTH):]

        for point_idx, i in enumerate(range(0, len(self._pos_history), TRAIL_PERIOD)):
            self._trail[point_idx].position = tuple(self._pos_history[i])

        self.draw(self.window)

    @staticmethod
    def draw_all(window):
        for body in Body.instances:
            body.draw(window)

    @staticmethod
    def update_all(frame):
        for body in Body.instances:
            body.update(frame)
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos_history.append(value / SCALE)
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
    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, color: str):
        super().__init__(pos=pos, vel=vel, mass=mass, radius=radius, color=color)
        self._renderable.set_color(color, gp.colors["white"], color, color)

    def update(self, frame):
        return


def rescale(mu):
    global SCALE
    SCALE = mu * 1.3e10 + (1 - mu) * 1e9
