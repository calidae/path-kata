from math import hypot, sqrt
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    p1: Point
    p2: Point


def distance(segment: Segment) -> float:
    dx = segment.p1.x - segment.p2.x
    dy = segment.p1.y - segment.p2.y
    return hypot(dx, dy)


def test_segment_distance() -> None:
    assert distance(Segment(Point(0, 0), Point(0, 1))) == 1
    assert distance(Segment(Point(0, 0), Point(1, 1))) == sqrt(2)
