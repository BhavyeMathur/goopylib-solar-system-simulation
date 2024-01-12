import goopylib as gp
import numpy as np

from . import mainloop


__rings: list[gp.Circle] = []
N = 0


def __create_rings(radii):
    for light in __rings:
        light.destroy()
    __rings.clear()

    for i in range(N):
        light = gp.Circle((0, 0), float(radii[i])).draw(mainloop.window)
        light.set_color(gp.Color("#edda8e"))
        light.z = 1
        __rings.append(light)


def __set_transparencies():
    for i, light in enumerate(__rings):
        light.transparency = (1 - i / N) ** (8 + 2 * np.cos(mainloop.frame / 30))


def init(n):
    global __rings, N

    N = n

    __create_rings(np.linspace(20, 100, n))
    __set_transparencies()


def shine():
    __set_transparencies()


def rescale(mu):
    mu = max(mu, 0.001) ** 0.2

    radii = np.linspace(mu * 1 + (1 - mu) * 20,
                        mu * 5 + (1 - mu) * 100, N)

    __create_rings(radii)
    __set_transparencies()
