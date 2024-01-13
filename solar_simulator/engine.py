from scipy.spatial.distance import pdist, squareform
import numpy as np

from .body import *

G = 6.67e-11

DT = 10000  # seconds
_DT_HOURS = DT / 3600
DT_MULTIPLIER = 1
T = 0  # hours

positions: np.ndarray
velocities: np.ndarray
Gm: np.ndarray


def init():
    global positions, velocities, Gm

    positions = np.array([body.pos for body in Body.instances])
    velocities = np.array([body.vel for body in Body.instances])
    Gm = G * np.array([body.mass for body in Body.instances])


def evolve():
    global T, positions, velocities
    T += _DT_HOURS

    distance_matrix = pdist(positions)
    distance_matrix *= distance_matrix * distance_matrix
    distance_matrix = squareform(distance_matrix)
    np.fill_diagonal(distance_matrix, 1.0)

    sep = positions[np.newaxis, :] - positions[:, np.newaxis]

    accelerations = np.einsum('ijk,ij->ik', sep, Gm / distance_matrix)
    velocities += DT * accelerations
    positions += DT * velocities

    for i, body in enumerate(Body.instances):
        if isinstance(body, StationaryBody):
            continue
        body.pos = positions[i].copy()


def recalculate_dt(mu=None):
    global DT, _DT_HOURS

    if mainloop.camera.follow_body is None:
        mu = (mu if mu else scroll.get_scale_interpolation_factor()) ** 3
        DT = mu * 100000 + (1 - mu) * 2500
    else:
        DT = mainloop.camera.follow_body.follow_dt

    DT = min((DT_MULTIPLIER * DT, 100000))
    _DT_HOURS = DT / 3600


def increase_dt(_):
    global DT_MULTIPLIER

    DT_MULTIPLIER = min(DT_MULTIPLIER * 1.1, 20)
    recalculate_dt()


def decrease_dt(_):
    global DT_MULTIPLIER

    DT_MULTIPLIER = max(DT_MULTIPLIER / 1.1, 0.1)
    recalculate_dt()


from . import scroll
from . import mainloop
