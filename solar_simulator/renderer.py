import goopylib.imports as gp

from .body import *
from . import mainloop
import math


__planets: dict[Body, gp.Circle] = {}
__trails: dict[Body, list[gp.Circle]] = {}

__camera = None
__scroll = 0
__scale = 1e9
__last_scale = __scale
mu = 0

TRAIL_LENGTH = 100
TRAIL_PERIOD = 2


def init(window):
    global __planets, __trails, __camera

    __camera = window.get_camera()

    __planets = {body: gp.Circle((0, 0), body.radius) for body in Body.instances}
    __trails = {body: [] for body in Body.instances}

    for planet, graphic in __planets.items():
        if isinstance(planet, StationaryBody):
            color = gp.Color(planet.color)
            graphic.set_color(color, gp.colors["white"], color, color)
        else:
            graphic.set_color(*get_planet_colors(planet.color))

            graphic.draw(window)


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
    for planet, graphic in __planets.items():
        if isinstance(planet, StationaryBody):
            # graphic.draw(graphic.window)
            continue

        graphic.x = planet.x / __scale
        graphic.y = planet.y / __scale

        theta = math.atan2(*planet.pos)
        graphic.rotation = math.degrees(theta) + 30

        if mainloop.frame % TRAIL_PERIOD == 0:
            point = gp.Circle(planet.pos / __scale, 1).draw(graphic.window)
            point.set_color(gp.colors["whitesmoke"])

            trail = __trails[planet]
            trail.append(point)

            alphas = np.linspace(0, 1, len(trail)) ** 2
            for i, item in enumerate(trail):
                item.set_transparency(alphas[i])

            if len(trail) > TRAIL_LENGTH:
                trail[0].destroy()
                trail.pop(0)

        graphic.draw(graphic.window)


def _update_trails():
    global __last_scale
    k = __scale / __last_scale

    for planet in __planets.keys():
        if isinstance(planet, StationaryBody):
            continue

        for trail in __trails[planet]:
            trail.x /= k
            trail.y /= k

    __last_scale = __scale


def zoom(scroll):
    global __scroll, __scale, mu, TRAIL_PERIOD

    scroll = max(-0.1, min(0.1, scroll ** 3))
    __scroll = min(max(__scroll + scroll, -4), 4)

    __scale = max(min(__scale * 2 ** scroll, 1.3e10), 1e9)
    mu = (__scale - 1e9) / (1.3e10 - 1e9)

    TRAIL_PERIOD = mu * 4 + (1 - mu) * 2

    __camera.zoom = 1 + 0.75 / (1 + 1 / np.exp(-__scroll))
    _update_trails()


orbit = draw
approach = zoom
