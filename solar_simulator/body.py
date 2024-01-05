import goopylib.imports as gp
import math

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
        
        self.graphic = gp.Circle((0, 0), self.radius)
        self.trail: list[gp.Circle] = []
    
    def draw(self, window):
        self.graphic.draw(window)
        # if isinstance(body, StationaryBody):
        #     color = gp.Color(planet.color)
        #     graphic.set_color(color, gp.colors["white"], color, color)
        # else:
        #     graphic.set_color(*get_planet_colors(planet.color))
        # 
        #     graphic.draw(window)

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y


class StationaryBody(Body):
    def __init__(self, pos: Vec2D, vel: Vec2D, mass: float, radius: float, color: str):
        super().__init__(pos=pos, vel=vel, mass=mass, radius=radius, color=color)


__camera = None
__scroll = 0
__scale = 1e9
__last_scale = __scale
mu = 0

TRAIL_LENGTH = 100
TRAIL_PERIOD = 2


def init(window):
    global __camera

    __camera = window.get_camera()

    for body in Body.instances:
        body.draw(window)


def get_planet_colors(color):
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


def draw():
    for body in Body.instances:
        if isinstance(body, StationaryBody):
            continue

        body.graphic.x = body.x / __scale
        body.graphic.y = body.y / __scale

        theta = math.atan2(*body.pos)
        body.graphic.rotation = math.degrees(theta) + 30

        # if mainloop.frame % TRAIL_PERIOD == 0:
        #     point = gp.Circle(body.pos / __scale, 1).draw(body.graphic.window)
        #     point.set_color(gp.colors["whitesmoke"])
        #
        #     trail = __trails[body]
        #     trail.append(point)
        #
        #     alphas = np.linspace(0, 1, len(trail)) ** 2
        #     for i, item in enumerate(trail):
        #         item.set_transparency(alphas[i])
        #
        #     if len(trail) > TRAIL_LENGTH:
        #         trail[0].destroy()
        #         trail.pop(0)

        body.graphic.draw(body.graphic.window)


def _update_trails():
    global __last_scale
    pass
    # k = __scale / __last_scale
    #
    # for planet in __planets.keys():
    #     if isinstance(planet, StationaryBody):
    #         continue
    #
    #     for trail in __trails[planet]:
    #         trail.x /= k
    #         trail.y /= k
    #
    # __last_scale = __scale


def zoom(scroll):
    global __scroll, __scale, mu, TRAIL_PERIOD

    scroll = max(-0.1, min(0.1, scroll ** 3))
    __scroll = min(max(__scroll + scroll, -4), 4)

    __scale = max(min(__scale * 2 ** scroll, 1.3e10), 1e9)
    mu = (__scale - 1e9) / (1.3e10 - 1e9)

    TRAIL_PERIOD = mu * 4 + (1 - mu) * 2

    __camera.zoom = 1 + 0.75 / (1 + 1 / np.exp(-__scroll))
    _update_trails()
