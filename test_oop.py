from math import hypot, sqrt
from operator import itemgetter
from functools import wraps
from typing import NamedTuple, List, Optional

import pytest


class Point(NamedTuple):
    x: int
    y: int


class Segment(object):
    __slots__ = ('_p1', '_p2')
    _p1: Point
    _p2: Point

    def __init__(self, p1: Point, p2: Point) -> None:
        if p1 == p2:
            raise ValueError("Points must be different")
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self) -> Point: return self._p1

    @property
    def p2(self) -> Point: return self._p2

    def distance(self) -> float:
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        return hypot(dx, dy)

    def __repr__(self):
        return 'Segment({},{})'.format(self.p1, self.p2)


class Path(object):
    __slots__ = ('_segments')
    _segments: List[Segment]

    def __init__(self, segments: List[Segment]) -> None:
        if not len(segments):
            raise ValueError("A Path must contain segments")
        self._segments = segments

    @property
    def segments(self) -> List[Segment]: return self._segments

    def distance(self) -> float:
        return sum((segment.distance() for segment in self.segments))

    def stops(self) -> List[Point]:
        return [
            segment.p1 for segment in self.segments
        ]+[self.segments[-1].p2]

    def __repr__(self):
        return 'Path({})'.format(', '.join((
            str(segment) for segment in self.segments
        )))


class PathList(object):
    __slots__ = ('_paths')
    _paths: List[Path]

    def __init__(self, paths: List[Path]) -> None:
        self._paths = paths

    @property
    def paths(self) -> List[Path]: return self._paths

    def _none_if_no_paths(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            return f(inst, *args, **kwargs) if inst.paths else None
        return wrapped

    @_none_if_no_paths
    def get_shortest_path(self) -> Optional[Path]:
        return min((
            (path, path.distance())
            for path in self.paths
        ), key=itemgetter(1))[0]

    def get_paths_with_stops(self, stops) -> List[Path]:
        return [
            path for path in self.paths
            if set(stops) <= set(path.stops())
        ]

    @_none_if_no_paths
    def get_shortest_path_with_stops(self, stops) -> Optional[Path]:
        return PathList(self.get_paths_with_stops(stops)).get_shortest_path()

    def __repr__(self):
        return 'PathList({})'.format(', '.join((
            str(path) for path in self.paths
        )))


def test_segment_same_points_error() -> None:
    with pytest.raises(ValueError):
        Segment(Point(0, 0), Point(0, 0))


def test_segment_distance() -> None:
    assert Segment(Point(0, 0), Point(0, 1)).distance() == 1
    assert Segment(Point(0, 0), Point(1, 1)).distance() == sqrt(2)


def test_empty_path_error() -> None:
    with pytest.raises(ValueError):
        Path([])


def test_path_distance() -> None:
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = Path([s1, s2])
    assert p1.distance() == 2 * sqrt(2)


def test_get_shortest_path() -> None:
    assert PathList([]).get_shortest_path() is None

    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = Path([s1, s2])
    p2 = Path([s1])

    path_list = PathList([p2, p1])
    assert path_list.get_shortest_path() == p2


def test_get_path_stops() -> None:
    s1 = Segment(Point(0, 0), Point(0, 1))
    p1 = Path([s1])
    assert p1.stops() == [Point(0, 0), Point(0, 1)]

    s2 = Segment(Point(0, 1), Point(1, 2))
    s3 = Segment(Point(1, 2), Point(3, 3))
    p2 = Path([s1, s2, s3])
    assert p2.stops() == [
        Point(0, 0), Point(0, 1), Point(1, 2), Point(3, 3)]


def test_get_paths_with_stops() -> None:
    stop_list = [Point(0, 0)]
    s1 = Segment(Point(0, 0), Point(0, 1))
    p1 = Path([s1])
    assert PathList([p1]).get_paths_with_stops(stop_list) == [p1]

    s2 = Segment(Point(1, 1), Point(2, 2))
    p2 = Path([s2])
    assert PathList([p1, p2]).get_paths_with_stops(stop_list) == [p1]

    assert PathList([p2]).get_paths_with_stops(stop_list) == []

    stop_list2 = [Point(0, 0), Point(1, 1)]
    assert PathList([p2]).get_paths_with_stops(stop_list2) == []


def test_get_shortest_path_with_stops() -> None:
    assert PathList([]).get_shortest_path_with_stops([]) is None

    s1 = Segment(Point(-4, -2), Point(0, 0))
    p1 = Path([s1])
    assert PathList([p1]).get_shortest_path_with_stops([]) == p1

    stop_list = [Point(0, 0), Point(0, 1)]
    s2 = Segment(Point(0, 0), Point(0, 1))
    p2 = Path([s1, s2])
    assert PathList([p1, p2]).get_shortest_path_with_stops(stop_list) == p2

    stop_list2 = [Point(42, 0)]
    assert PathList([p1, p2]).get_shortest_path_with_stops(stop_list2) is None
