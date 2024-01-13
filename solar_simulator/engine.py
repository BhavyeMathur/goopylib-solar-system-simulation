from scipy.spatial.distance import pdist, squareform
import numpy as np

from .body import *

G = 6.67e-11
DT = 10000  # seconds
DT_MULTIPLIER = 1
T = 0  # hours

_DT_HOURS = DT / 3600

Fx: np.ndarray
Fy: np.ndarray
positions: np.ndarray
velocities: np.ndarray
Gm: np.ndarray


def init():
    global Fx, Fy, positions, velocities, Gm

    Fx = np.array([[0 for other in Body.instances if other != body] for body in Body.instances])
    Fy = Fx.copy()

    positions = np.array([body.pos for body in Body.instances])
    velocities = np.array([body.vel for body in Body.instances])
    Gm = G * np.array([body.mass for body in Body.instances])


def evolve():
    global T, Fx, Fy, positions, velocities
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
        body.pos = positions[i].copy()


def calculate_dt(mu, body):
    global DT, _DT_HOURS

    if body is None:
        mu **= 3
        DT = mu * 100000 + (1 - mu) * 2500
    else:
        DT = body.follow_dt

    DT = min((DT_MULTIPLIER * DT, 100000))
    _DT_HOURS = DT / 3600
