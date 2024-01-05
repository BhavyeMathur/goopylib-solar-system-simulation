from .body import *
import math


G = 6.67e-11
DT = 10000  # seconds
DT_MULTIPLIER = 1
T = 0  # hours


def evolve():
    global T
    T += DT / 3600

    for body in Body.instances:
        if isinstance(body, StationaryBody):
            continue

        ax = 0
        ay = 0

        for other in Body.instances:
            if body == other:
                continue

            distance = max(abs(other.pos - body.pos), 1e-3)
            theta = math.atan2(*(other.pos - body.pos))

            a = G * other.mass / (distance ** 2)
            ax += math.sin(theta) * a
            ay += math.cos(theta) * a

        body.vel += Vector2D(ax, ay) * DT
        body.pos += body.vel * DT


def calculate_dt(mu):
    global DT

    mu **= 3
    DT = min((mu * 100000 + (1 - mu) * 2500) * DT_MULTIPLIER, 100000)
