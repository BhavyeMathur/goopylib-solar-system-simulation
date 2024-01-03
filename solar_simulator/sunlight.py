import goopylib as gp
import numpy as np

__rings: list[gp.Circle] = []
__frame = 0
__window = None
__N = 0


def __create_rings(radii):
    for light in __rings:
        light.destroy()
    __rings.clear()

    for i in range(__N):
        light = gp.Circle((0, 0), float(radii[i])).draw(__window)
        light.set_color(gp.Color("#edda8e"))
        __rings.append(light)


def __set_transparencies():
    for i, light in enumerate(__rings):
        light.set_transparency((1 - i / __N) ** (8 + 2 * np.cos(__frame / 30)))


def init(n, window):
    global __rings, __window, __N

    __N = n
    __window = window

    __create_rings(np.linspace(20, 100, n))
    __set_transparencies()


def shine():
    global __frame
    __frame += 1
    __set_transparencies()


def expand(mu):
    mu = max(mu, 0.001) ** 0.25

    radii = np.linspace(mu * 1 + (1 - mu) * 20,
                        mu * 5 + (1 - mu) * 100, __N)

    __create_rings(radii)
    __set_transparencies()
