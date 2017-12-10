from math import hypot, sqrt
from typing import NamedTuple, List, Optional
from operator import itemgetter

from toolz.itertoolz import first


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    p1: Point
    p2: Point


Path = List[Segment]
PathList = List[Path]


def distance(segment: Segment) -> float:
    dx = segment.p1.x - segment.p2.x
    dy = segment.p1.y - segment.p2.y
    return hypot(dx, dy)


def total_distance(path: Path) -> float:
    return sum((distance(segment) for segment in path))


def shortest_path(path_list: PathList) -> Optional[Path]:
    return first(min((
        (path, total_distance(path))
        for path in path_list
    ), key=itemgetter(1), default=[None]))


def test_segment_distance() -> None:
    assert distance(Segment(Point(0, 0), Point(0, 1))) == 1
    assert distance(Segment(Point(0, 0), Point(1, 1))) == sqrt(2)


def test_path_distance() -> None:
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    assert total_distance([s1, s2]) == 2 * sqrt(2)


def test_shortest_path() -> None:
    assert shortest_path([]) is None

    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = [s1, s2]
    p2 = [s1]

    path_list = [p2, p1]
    assert shortest_path(path_list) == p2
