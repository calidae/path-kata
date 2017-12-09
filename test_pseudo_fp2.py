from math import hypot, sqrt
from typing import NamedTuple, List


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    p1: Point
    p2: Point


Path = List[Segment]


def distance(segment: Segment) -> float:
    dx = segment.p1.x - segment.p2.x
    dy = segment.p1.y - segment.p2.y
    return hypot(dx, dy)


def total_distance(path: Path) -> float:
    return sum((distance(segment) for segment in path))


def test_segment_distance() -> None:
    assert distance(Segment(Point(0, 0), Point(0, 1))) == 1
    assert distance(Segment(Point(0, 0), Point(1, 1))) == sqrt(2)


def test_path_distance() -> None:
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    assert total_distance([s1, s2]) == 2 * sqrt(2)
