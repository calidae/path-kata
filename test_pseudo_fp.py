from math import sqrt
from collections import namedtuple

Point = namedtuple('Point', ('x', 'y'))
Segment = namedtuple('Segment', ('p1', 'p2'))


def segment_distance(segment):
    return sqrt(
        ((segment.p1.x - segment.p2.x)**2) +
        ((segment.p1.y - segment.p2.y)**2)
    )


def path_distance(path):
    return sum((
        segment_distance(segment)
        for segment in path
    ))


def get_shortest_path(path_list):
    return min((
        (path, path_distance(path))
        for path in path_list
    ), key=lambda x: x[1])[0]


def get_path_stops(path):
    return [
        segment.p1
        for segment in path
    ]+[path[-1].p2]


def get_paths_with_stops(path_list, stop_list):
    return [
        path for path in path_list
        if set(stop_list) <= set(get_path_stops(path))
    ]


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
