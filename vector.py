import numpy as np

Vec2D = tuple[float, float]


class Vector2D(np.ndarray):
    def __new__(cls, x: float, y: float):
        obj = np.asarray([x, y], dtype="float32").view(cls)
        return obj

    def __repr__(self):
        return f"Vec2D({self})"

    def __abs__(self):
        return sum(self ** 2) ** 0.5

    def __ge__(self, other):
        return abs(self) >= abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __le__(self, other):
        return abs(self) <= abs(other)

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __bool__(self):
        return abs(self) > 0

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value
