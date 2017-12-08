from math import hypot, sqrt
from collections import namedtuple
from operator import itemgetter

import pytest


Point = namedtuple('Point', ('x', 'y'))


class Segment(object):
    __slots__ = ('_p1', '_p2')

    def __init__(self, p1, p2):
        if p1 == p2:
            raise ValueError("Points must be different")
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self): return self._p1

    @property
    def p2(self): return self._p2

    def distance(self):
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        return hypot(dx, dy)


class Path(object):
    __slots__ = ('_segments')

    def __init__(self, segments):
        self._segments = segments

    @property
    def segments(self): return self._segments

    def distance(self):
        return sum((segment.distance() for segment in self.segments))


class PathList(object):
    __slots__ = ('_paths')

    def __init__(self, paths):
        self._paths = paths

    @property
    def paths(self): return self._paths

    def get_shortest_path(self):
        return min((
            (path, path.distance())
            for path in self._paths
        ), key=itemgetter(1))[0]


def test_segment_same_points_error():
    with pytest.raises(ValueError):
        Segment(Point(0, 0), Point(0, 0))


def test_segment_distance():
    assert Segment(Point(0, 0), Point(0, 1)).distance() == 1
    assert Segment(Point(0, 0), Point(1, 1)).distance() == sqrt(2)


def test_path_distance():
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = Path([s1, s2])
    assert p1.distance() == 2 * sqrt(2)

    p2 = Path([])
    assert p2.distance() == 0


def test_get_shortest_path():
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = Path([s1, s2])
    p2 = Path([s1])

    path_list = PathList([p2, p1])
    assert path_list.get_shortest_path() == p2
