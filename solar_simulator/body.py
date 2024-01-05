import goopylib.imports as gp
import math

from .vector import *


TRAIL_LENGTH = 100
TRAIL_PERIOD = 2

SCALE = 1e9


class Body(gp.Circle):
    instances = []

    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, color: str):
        super().__init__((0, 0), radius)
        self.set_color(*self.get_color(color))

        self.pos = Vector2D(*pos)
        self.vel = Vector2D(*vel)

        self.mass = mass
        self.radius = radius

        Body.instances.append(self)
        self.trail: list[gp.Circle] = []

    @staticmethod
    def get_color(color):
        shadow = list(gp.hex_to_hsv(color))
        shadow[2] = max(shadow[2] - 0.3, 0)
        shadow[1] = min(shadow[1] + 0.3, 1)
        shadow = gp.Color(gp.hsv_to_hex(*shadow))

        albedo = list(gp.hex_to_hsv(color))
        albedo[2] = min(albedo[2] + 0.3, 1)
        albedo[1] = max(albedo[1] - 0.3, 0)
        albedo = gp.Color(gp.hsv_to_hex(*albedo))

        color = gp.Color(color)

        return color, albedo, shadow, gp.colors["black"]

    def update(self):
        self.x = self.pos.x / SCALE
        self.y = self.pos.y / SCALE

        theta = math.atan2(*self.pos)
        self.rotation = math.degrees(theta) + 30

        # if mainloop.frame % TRAIL_PERIOD == 0:
        #     point = gp.Circle(self.pos / SCALE, 1).draw(self.graphic.window)
        #     point.set_color(gp.colors["whitesmoke"])
        #
        #     trail = __trails[self]
        #     trail.append(point)
        #
        #     alphas = np.linspace(0, 1, len(trail)) ** 2
        #     for i, item in enumerate(trail):
        #         item.set_transparency(alphas[i])
        #
        #     if len(trail) > TRAIL_LENGTH:
        #         trail[0].destroy()
        #         trail.pop(0)

        self.draw(self.window)
    
    # def draw(self, window):
        # if isinstance(body, StationaryBody):
        #     color = gp.Color(planet.color)
        #     graphic.set_color(color, gp.colors["white"], color, color)
        # else:
        #     graphic.set_color(*get_planet_colors(planet.color))
        # 
        #     graphic.draw(window)


class StationaryBody(Body):
    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, color: str):
        super().__init__(pos=pos, vel=vel, mass=mass, radius=radius, color=color)
        self.set_color(color, gp.colors["white"], color, color)

    def update(self):
        return


def init(window):
    global CAMERA
    CAMERA = window.get_camera()

    for body in Body.instances:
        body.draw(window)


def orbit():
    for body in Body.instances:
        body.update()


def _update_trails():
    pass
    # k = SCALE / LAST_SCALE
    #
    # for planet in __planets.keys():
    #     if isinstance(planet, StationaryBody):
    #         continue
    #
    #     for trail in __trails[planet]:
    #         trail.x /= k
    #         trail.y /= k
    #
    # LAST_SCALE = SCALE


def zoom(mu):
    global TRAIL_PERIOD

    TRAIL_PERIOD = mu * 4 + (1 - mu) * 2
    _update_trails()
