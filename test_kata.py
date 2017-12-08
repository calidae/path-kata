from math import sqrt

from kata import Segment
from kata import Point
from kata import segment_distance
from kata import path_distance
from kata import get_shortest_path
from kata import get_path_stops
from kata import get_paths_with_stops


def test_segment_distance():
    s1 = Segment(Point(0, 0), Point(0, 0))
    assert segment_distance(s1) == 0

    s2 = Segment(Point(0, 0), Point(0, 1))
    assert segment_distance(s2) == 1

    s3 = Segment(Point(0, 0), Point(1, 1))
    assert segment_distance(s3) == sqrt(2)


def test_path_distance():
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = [s1, s2]
    assert path_distance(p1) == 2 * sqrt(2)

    p2 = []
    assert path_distance(p2) == 0


def test_get_shortest_path():
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 2))
    p1 = [s1, s2]
    p2 = [s1]

    path_list = [p2, p1]
    assert get_shortest_path(path_list) == p2


def test_get_path_stops():
    s1 = Segment(Point(0, 0), Point(0, 1))
    p1 = [s1]
    assert get_path_stops(p1) == [Point(0, 0), Point(0, 1)]

    s2 = Segment(Point(0, 1), Point(1, 2))
    s3 = Segment(Point(1, 2), Point(3, 3))
    p2 = [s1, s2, s3]
    assert get_path_stops(p2) == [
        Point(0, 0), Point(0, 1), Point(1, 2), Point(3, 3)]


def test_get_paths_with_stops():
    stop_list = [Point(0, 0)]
    s1 = Segment(Point(0, 0), Point(0, 1))
    p1 = [s1]
    assert get_paths_with_stops([p1], stop_list) == [p1]

    s2 = Segment(Point(1, 1), Point(2, 2))
    p2 = [s2]
    assert get_paths_with_stops([p1, p2], stop_list) == [p1]

    assert get_paths_with_stops([p2], stop_list) == []

    stop_list2 = [Point(0, 0), Point(1, 1)]
    assert get_paths_with_stops([p2], stop_list2) == []
