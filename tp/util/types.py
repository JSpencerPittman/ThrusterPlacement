from dataclasses import dataclass


@dataclass
class Point(object):
    x: float
    y: float


Points = list[Point]
Polygon = Points


@dataclass
class Rectangle(object):
    """
    (x, y) should describe the top-left corner.
    """

    x: float
    y: float
    w: float
    h: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.h
