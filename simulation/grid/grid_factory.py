"""
Created at 22.08.2019

@author: Michał Jureczka
@author: Piotr Bartman
"""

import numpy as np
from simulation.grid.grid import Grid


class GridFactory:
    @staticmethod
    def addPoint(grid, x, y, t):
        i = 0
        while i < len(grid.Points):
            if grid.Points[i][0] == x and grid.Points[i][1] == y:
                return
            else:
                i += 1
        grid.Points = np.append([[x, y, t]], grid.Points, axis=0)
        for i in range(len(grid.Edges)):
            grid.Edges[i][0] += 1
            grid.Edges[i][1] += 1

    @staticmethod
    def addEdge(grid, i, j, t):  # (i,j): xi <= xj and yi < yj
        a = i
        b = j
        if (grid.Points[j][0] < grid.Points[i][0] or
                (grid.Points[j][0] == grid.Points[i][0] and grid.Points[j][1] < grid.Points[i][1])):
            a = j
            b = i
        grid.Edges = np.append([[a, b, t]], grid.Edges, axis=0)

    @staticmethod
    def startBorder(grid, x, y):
        GridFactory.addPoint(grid, x, y, 0)

    @staticmethod
    def addBorderD(grid, x, y):
        GridFactory.addPoint(grid, x, y, 1)
        GridFactory.addEdge(grid, 1, 0, 2)
        grid.BorderEdgesD += 1

    @staticmethod
    def addBorderDLast(grid, x, y):
        GridFactory.addPoint(grid, x, y, 2)
        GridFactory.addEdge(grid, 1, 0, 2)
        grid.BorderEdgesD += 1

    @staticmethod
    def addBorderNTop(grid, x, y):
        GridFactory.addPoint(grid, x, y, 3)
        GridFactory.addEdge(grid, 1, 0, 1)
        grid.BorderEdgesD += 1

    @staticmethod
    def addBorderNTopLast(grid, x, y):
        GridFactory.addPoint(grid, x, y, 4)
        GridFactory.addEdge(grid, 1, 0, 1)
        grid.BorderEdgesD += 1

    @staticmethod
    def addBorderNSide(grid, x, y):
        GridFactory.addPoint(grid, x, y, 5)
        GridFactory.addEdge(grid, 0, 1, 2)
        grid.BorderEdgesD += 1

    @staticmethod
    def addBorderNSideLast(grid, x, y):
        GridFactory.addPoint(grid, x, y, 6)
        GridFactory.addEdge(grid, 0, 1, 2)
        grid.BorderEdgesD += 1

    @staticmethod
    def addBorderC(grid, x, y):
        GridFactory.addPoint(grid, x, y, 7)
        GridFactory.addEdge(grid, 0, 1, 1)
        grid.BorderEdgesC += 1

    @staticmethod
    def stopBorder(grid):
        GridFactory.addEdge(grid, len(grid.Points) - 1, 0, 1)
        grid.BorderEdgesC += 1

    @staticmethod
    def construct(sizeH, sizeL, height):
        grid = Grid()
        grid.SizeH = sizeH
        grid.SizeL = sizeL
        grid.Height = float(height)
        grid.longTriangleSide = grid.Height / sizeH
        grid.Length = grid.longTriangleSide * sizeL

        grid.halfLongTriangleSide = grid.longTriangleSide * 0.5
        grid.shortTriangleSide = grid.longTriangleSide * np.sqrt(2.) * 0.5
        grid.halfShortTriangleSide = grid.shortTriangleSide * 0.5
        grid.TriangleArea = (grid.longTriangleSide * grid.longTriangleSide) / 4.

        GridFactory.startBorder(grid, 0, 0)

        for i in range(1, sizeH):
            GridFactory.addBorderD(grid, 0, float(i) * grid.longTriangleSide)
        GridFactory.addBorderDLast(grid, 0, float(sizeH) * grid.longTriangleSide)

        for i in range(1, sizeL):
            GridFactory.addBorderNTop(grid, float(i) * grid.longTriangleSide, grid.Height)
        GridFactory.addBorderNTopLast(grid, float(sizeL) * grid.longTriangleSide, grid.Height)

        for i in range(sizeH - 1, 0, -1):
            GridFactory.addBorderNSide(grid, grid.Length, float(i) * grid.longTriangleSide)
        GridFactory.addBorderNSideLast(grid, grid.Length, 0.)

        for i in range(sizeL - 1, 0, -1):
            GridFactory.addBorderC(grid, float(i) * grid.longTriangleSide, 0)

        GridFactory.stopBorder(grid)

        for i in range(sizeL):
            for j in range(1, sizeH):
                x1 = float(i) * grid.longTriangleSide
                x2 = float(i + 1) * float(grid.longTriangleSide)
                y = float(j) * grid.longTriangleSide
                GridFactory.addPoint(grid, x1, y, 8)
                GridFactory.addPoint(grid, x2, y, 8)
                a = grid.getPoint(x1, y)
                b = grid.getPoint(x2, y)
                GridFactory.addEdge(grid, a, b, 1)

        for i in range(1, sizeL):
            for j in range(sizeH):
                x = float(i) * grid.longTriangleSide
                y1 = float(j) * grid.longTriangleSide
                y2 = float(j + 1) * grid.longTriangleSide
                GridFactory.addPoint(grid, x, y1, 8)
                GridFactory.addPoint(grid, x, y2, 8)
                a = grid.getPoint(x, y1)
                b = grid.getPoint(x, y2)
                GridFactory.addEdge(grid, a, b, 2)

        for i in range(sizeL):
            for j in range(sizeH):
                x = (float(i) + 0.5) * grid.longTriangleSide
                y = (float(j) + 0.5) * grid.longTriangleSide
                GridFactory.addPoint(grid, x, y, 9)
                a = grid.getPoint(x, y)
                b = grid.getPoint((float(i)) * grid.longTriangleSide, (float(j) + 1.0) * grid.longTriangleSide)
                GridFactory.addEdge(grid, a, b, 5)
                b = grid.getPoint((float(i) + 1.0) * grid.longTriangleSide, (float(j) + 1.0) * grid.longTriangleSide)
                GridFactory.addEdge(grid, a, b, 4)
                b = grid.getPoint((float(i) + 1.0) * grid.longTriangleSide, (float(j)) * grid.longTriangleSide)
                GridFactory.addEdge(grid, a, b, 6)
                b = grid.getPoint((float(i)) * grid.longTriangleSide, (float(j)) * grid.longTriangleSide)
                GridFactory.addEdge(grid, a, b, 3)

        max_edges = 4
        grid.edges = np.zeros((np.max(grid.Edges) + 1, max_edges, 2), dtype=np.int)
        grid.edges -= 1
        for i in range(len(grid.Edges)):
            edges = grid.edges[grid.Edges[i][0]]
            for j in range(max_edges):
                if edges[j][0] == -1:
                    edges[j][0] = grid.Edges[i][1]
                    edges[j][1] = grid.Edges[i][2]
                    break
        return grid
