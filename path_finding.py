# Pathfinding algorithm, simple implementation of A*
import math


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, end):
    pass
