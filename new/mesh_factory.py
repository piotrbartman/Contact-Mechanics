"""
Created at 30.10.2019

@author: Michał Jureczka
@author: Piotr Bartman
"""

from new.point import Point
from new.edge import Edge
from new.element import Element
from new.mesh import Mesh
from new.constants import *


class Regular2D:
    @staticmethod
    def construct(size: int, dx: int, left, top, right, bottom) -> Mesh:

        n_size = size // dx
        dimension = 2

        point = Regular2D.create_point(dimension, n_size, dx)
        edge = Regular2D.edge(dimension, n_size)
        element = Regular2D.element(dimension, n_size)

        subarea = {'border': {}}
        subarea['border']['left'] = edge[0: n_size - 1]
        subarea['border']['right'] = edge[(n_size - 1) ** 2: (n_size - 1) ** 2 + n_size - 1]
        subarea['border']['bottom'] = edge[(n_size - 1) ** 2 + n_size: 2 * (n_size - 1) * n_size: n_size]
        subarea['border']['top'] = edge[(n_size - 1) ** 2 + 2 * n_size - 1: 2 * (n_size - 1) * n_size: n_size]

        mesh = Mesh(point, edge, element, subarea)

        return mesh

    @staticmethod
    def create_point(dimension: int, n_size: int, dx: float) -> Point:

        n_points = n_size ** 2 + (n_size - 1) ** 2
        point = Point(dimension, n_points)

        point_i = 0
        x = 0
        y = 0
        dy = dx
        for j in range(n_size):
            for i in range(n_size):
                point[point_i][0] = x
                point[point_i][1] = y
                x += dx
                point_i += 1
            y += dy
            x = 0

        x = .5 * dx
        y = .5 * dy
        dy = dx
        for j in range(n_size - 1):
            for i in range(n_size - 1):
                point[point_i][0] = x
                point[point_i][1] = y
                x += dx
                point_i += 1
            y += dy
            x = .5 * dx

        return point

    @staticmethod
    def edge(dimension: int, n_size: int) -> Edge:

        n_edges = 2 * (n_size - 1) * n_size + 4 * (n_size - 1) ** 2
        edge = Edge(dimension, n_edges)

        edge_i = 0
        for j in range(n_size):
            for i in range(n_size - 1):
                edge[edge_i][0] = n_size * j + i
                edge[edge_i][1] = n_size * j + (i + 1)
                edge_i += 1

        for j in range(n_size - 1):
            for i in range(n_size):
                edge[edge_i][0] = n_size * j + i
                edge[edge_i][1] = n_size * (j + 1) + i
                edge_i += 1

        for j in range(n_size - 1):
            for i in range(n_size - 1):
                edge[edge_i][0] = n_size ** 2 + (n_size - 1) * j + i
                edge[edge_i][1] = n_size * j + i
                edge_i += 1
                edge[edge_i][0] = n_size ** 2 + (n_size - 1) * j + i
                edge[edge_i][1] = n_size * j + (i + 1)
                edge_i += 1
                edge[edge_i][0] = n_size ** 2 + (n_size - 1) * j + i
                edge[edge_i][1] = n_size * (j + 1) + (i + 1)
                edge_i += 1
                edge[edge_i][0] = n_size ** 2 + (n_size - 1) * j + i
                edge[edge_i][1] = n_size * (j + 1) + i
                edge_i += 1

        return edge

    @staticmethod
    def element(dimension: int, n_size: int) -> Element:

        n_elements = 4 * (n_size - 1) ** 2
        element = Element(dimension, n_elements)

        element_i = 0
        for j in range(n_size - 1):
            for i in range(n_size - 1):
                element[element_i][0] = (n_size - 1) * j + i
                element[element_i][1] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 0
                element[element_i][2] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 1
                element_i += 1
                element[element_i][0] = n_size * j + n_size * (n_size - 1) + 1 + i
                element[element_i][1] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 1
                element[element_i][2] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 2
                element_i += 1
                element[element_i][0] = (n_size - 1) * j + n_size - 1 + i
                element[element_i][1] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 2
                element[element_i][2] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 3
                element_i += 1
                element[element_i][0] = n_size * j + n_size * (n_size - 1) + i
                element[element_i][1] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 3
                element[element_i][2] = 2 * (n_size * (n_size - 1)) + j * (4 * (n_size - 1)) + 4 * i + 0
                element_i += 1

        return element

    @staticmethod
    def border(left, top, right, bottom):
        pass  # TODO