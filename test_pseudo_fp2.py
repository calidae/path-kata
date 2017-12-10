from math import hypot, sqrt
from typing import NamedTuple, List, Optional, Callable
from operator import itemgetter

from toolz.itertoolz import first, last
from toolz.functoolz import compose


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


def stops(path: Path) -> List[Point]:
    return [segment.p1 for segment in path]+[last(path).p2]


def paths_with_stops(path_list: PathList, stops_: List[Point]) -> PathList:
    return [
        path for path in path_list
        if set(stops_) <= set(stops(path))
    ]


shortest_path_with_stops: Callable[
    [PathList, List[Point]], Optional[Path]
] = compose(shortest_path, paths_with_stops)


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


def test_get_path_stops() -> None:
    s1 = Segment(Point(0, 0), Point(0, 1))
    p1 = [s1]
    assert stops(p1) == [Point(0, 0), Point(0, 1)]

    s2 = Segment(Point(0, 1), Point(1, 2))
    s3 = Segment(Point(1, 2), Point(3, 3))
    p2 = [s1, s2, s3]
    assert stops(p2) == [
        Point(0, 0), Point(0, 1), Point(1, 2), Point(3, 3)]


def test_get_paths_with_stops() -> None:
    stop_list = [Point(0, 0)]
    s1 = Segment(Point(0, 0), Point(0, 1))
    p1 = [s1]
    assert paths_with_stops([p1], stop_list) == [p1]

    s2 = Segment(Point(1, 1), Point(2, 2))
    p2 = [s2]
    assert paths_with_stops([p1, p2], stop_list) == [p1]

    assert paths_with_stops([p2], stop_list) == []

    stop_list2 = [Point(0, 0), Point(1, 1)]
    assert paths_with_stops([p2], stop_list2) == []


def test_get_shortest_path_with_stops() -> None:
    assert shortest_path_with_stops([], []) is None

    s1 = Segment(Point(-4, -2), Point(0, 0))
    p1 = [s1]
    assert shortest_path_with_stops([p1], []) == p1

    stop_list = [Point(0, 0), Point(0, 1)]
    s2 = Segment(Point(0, 0), Point(0, 1))
    p2 = [s1, s2]
    assert shortest_path_with_stops([p1, p2], stop_list) == p2

    stop_list2 = [Point(42, 0)]
    assert shortest_path_with_stops([p1, p2], stop_list2) is None