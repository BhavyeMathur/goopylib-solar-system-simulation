from .vector import *


class Body:
    instances = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, color: str):
        self.pos = Vector2D(*pos)
        self.vel = Vector2D(*vel)

        self.mass = mass

        self.radius = radius
        self.color = color

        Body.instances.append(self)

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y


class StationaryBody(Body):
    def __init__(self, pos: Vec2D, mass: float, radius: float, color: str):
        super().__init__(pos=pos, vel=(0, 0), mass=mass, radius=radius, color=color)
