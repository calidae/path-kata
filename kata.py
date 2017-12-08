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
        if set(stop_list) & set(get_path_stops(path))
    ]
