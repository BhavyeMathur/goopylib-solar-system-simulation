import goopylib.imports as gp

TRAIL_LENGTH = 100


class Trail:
    def __init__(self, trail_period):
        self.trail_period = trail_period
        self.last_trail_t = 0

        self.pos_history = []

        self.trail: list[gp.Circle] = [gp.Circle((0, 0), 1) for _ in range(TRAIL_LENGTH)]
        for i, point in enumerate(self.trail):
            point.set_color(gp.colors["whitesmoke"])
            point.transparency = i / TRAIL_LENGTH

    def draw(self, window):
        for point in self.trail:
            point.draw(window)

    def update(self):
        for i in range(0, min(len(self.pos_history), TRAIL_LENGTH)):
            self.trail[i].position = tuple(self.pos_history[i] / body.SCALE)

    def add_position(self, value):
        if universe.T - self.last_trail_t > self.trail_period:
            self.pos_history.append(value)
            self.last_trail_t = universe.T

            if len(self.pos_history) > TRAIL_LENGTH:
                self.pos_history.pop(0)


from . import body
from . import engine as universe
