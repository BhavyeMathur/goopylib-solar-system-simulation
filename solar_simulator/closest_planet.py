import math

import goopylib.imports as gp


class ClosestLine(gp.Line):
    instances = []
    draw_closest = True

    def __init__(self, planet):
        super().__init__((0, 0), (0, 0), thickness=1)
        self.set_color(gp.colors["whitesmoke"])
        self.transparency = 0.3
        self.planet = planet
        ClosestLine.instances.append(self)

    def update(self):
        if closest_body := self._find_closest_body():
            self.p1 = self.planet.position
            self.p2 = (closest_body.pos.x / body.SCALE, closest_body.pos.y / body.SCALE)

    def _find_closest_body(self):
        closest_dist = float("inf")
        closest_body = None

        for obj in Body.instances:
            if isinstance(obj, StationaryBody) or obj == self.planet:
                continue

            if (dist := math.dist(self.planet.position, obj.position)) < closest_dist:
                closest_dist = dist
                closest_body = obj

        return closest_body


def toggle_draw_closest(clicked):
    if not clicked:
        ClosestLine.draw_closest = not ClosestLine.draw_closest

    for obj in ClosestLine.instances:
        obj.hide(not ClosestLine.draw_closest)


from .body import Body, StationaryBody
from . import body
