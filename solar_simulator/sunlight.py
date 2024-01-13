import goopylib as gp
import numpy as np

from . import mainloop


rings: list[gp.Circle] = []
N = 0


def _create_rings(radii):
    for light in rings:
        light.destroy()
    rings.clear()

    for i in range(N):
        light = gp.Circle((0, 0), float(radii[i])).draw(mainloop.window)
        light.set_color("#edda8e")
        light.z = 1
        rings.append(light)


def _set_transparencies():
    for i, light in enumerate(rings):
        light.transparency = (1 - i / N) ** (8 + 2 * np.cos(mainloop.frame / 30))


def init(n):
    global rings, N

    N = n

    _create_rings(np.linspace(20, 100, n))
    _set_transparencies()


def shine():
    _set_transparencies()


def rescale(mu):
    mu = max(mu, 0.001) ** 0.2

    radii = np.linspace(mu * 1 + (1 - mu) * 20,
                        mu * 5 + (1 - mu) * 100, N)

    _create_rings(radii)
    _set_transparencies()
