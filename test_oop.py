from math import hypot, sqrt
from collections import namedtuple

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


def test_segment_same_points_error():
    with pytest.raises(ValueError):
        Segment(Point(0, 0), Point(0, 0))


def test_segment_distance():
    assert Segment(Point(0, 0), Point(0, 1)).distance() == 1
    assert Segment(Point(0, 0), Point(1, 1)).distance() == sqrt(2)
