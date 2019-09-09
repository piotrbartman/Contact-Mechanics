"""
Created at 21.08.2019

@author: Michał Jureczka
@author: Piotr Bartman
"""

import matplotlib.pyplot as plt
import pylab
import numpy as np


class Drawer:
    @staticmethod
    def draw(solver, setup, path=None, fixed_contact=False, verbose=True):
        mesh = solver.mesh
        title = f"Mesh[{mesh.SizeH}, {mesh.SizeL}] b[{setup.b}]"
        title += f" alpha[{setup.alpha}]" if not fixed_contact else ""

        plt.close()
        pylab.axes().set_aspect('equal', 'box')

        shadow = 0.1
        thickness1 = thickness2 = 2

        i = len(mesh.Edges) - 1
        j = len(mesh.Edges) - mesh.borders["Dirichlet"] - 1
        while j < i:
            x1 = mesh.Points[int(mesh.Edges[i, 0])][0]
            y1 = mesh.Points[int(mesh.Edges[i, 0])][1]
            x2 = mesh.Points[int(mesh.Edges[i, 1])][0]
            y2 = mesh.Points[int(mesh.Edges[i, 1])][1]
            plt.plot([x1, x2], [y1, y2], 'k-', alpha=shadow, lw=thickness1)
            i -= 1
        j -= mesh.borders["Neumann"]
        while j < i:
            x1 = mesh.Points[int(mesh.Edges[i, 0])][0]
            y1 = mesh.Points[int(mesh.Edges[i, 0])][1]
            x2 = mesh.Points[int(mesh.Edges[i, 1])][0]
            y2 = mesh.Points[int(mesh.Edges[i, 1])][1]
            plt.plot([x1, x2], [y1, y2], 'k-', alpha=shadow, lw=thickness1)
            i -= 1
        j -= mesh.borders["Contact"]
        while j < i:
            x1 = mesh.Points[int(mesh.Edges[i, 0])][0]
            y1 = mesh.Points[int(mesh.Edges[i, 0])][1]
            x2 = mesh.Points[int(mesh.Edges[i, 1])][0]
            y2 = mesh.Points[int(mesh.Edges[i, 1])][1]
            plt.plot([x1, x2], [y1, y2], 'k-', alpha=shadow, lw=thickness1)
            i -= 1
        while -1 < i:
            x1 = mesh.Points[int(mesh.Edges[i, 0])][0]
            y1 = mesh.Points[int(mesh.Edges[i, 0])][1]
            x2 = mesh.Points[int(mesh.Edges[i, 1])][0]
            y2 = mesh.Points[int(mesh.Edges[i, 1])][1]
            plt.plot([x1, x2], [y1, y2], 'k-', alpha=shadow, lw=thickness1)
            i -= 1

            # ------------
        fixed_u = np.zeros(solver.mesh.borders["Dirichlet"] + mesh.dirichlet_closure)
        if fixed_contact:
            fixed_u = np.concatenate((np.full(solver.mesh.borders["Contact"] - 1, solver.b), fixed_u))
        u = np.concatenate((solver.u, fixed_u))
        plt.scatter(mesh.Points[:, 0], mesh.Points[:, 1], marker='o', s=64, c=u, cmap="Reds")

        plt.clim(0, solver.b)
        plt.colorbar()

        # i = len(mesh.Edges) - 1
        # j = len(mesh.Edges) - mesh.borders["Dirichlet"] - 1
        # while j < i:
        #     x1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][0]
        #     y1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][1]
        #     x2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][0]
        #     y2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][1]
        #     plt.plot([x1, x2], [y1, y2], 'r-', lw=thickness2)
        #     i -= 1
        # j -= mesh.borders["Neumann"]
        # while j < i:
        #     x1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][0]
        #     y1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][1]
        #     x2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][0]
        #     y2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][1]
        #     plt.plot([x1, x2], [y1, y2], 'b-', lw=thickness2)
        #     i -= 1
        # j -= mesh.borders["Contact"]
        # while j < i:
        #     x1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][0]
        #     y1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][1]
        #     x2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][0]
        #     y2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][1]
        #     plt.plot([x1, x2], [y1, y2], 'y-', lw=thickness2)
        #     i -= 1
        # while -1 < i:
        #     x1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][0]
        #     y1 = solver.DisplacedPoints[int(mesh.Edges[i, 0])][1]
        #     x2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][0]
        #     y2 = solver.DisplacedPoints[int(mesh.Edges[i, 1])][1]
        #     plt.plot([x1, x2], [y1, y2], 'k-', lw=thickness2)
        #     i -= 1

            # ------------

        if path is not None:
            plot_path = path + "/" + title + '.png'
            plt.savefig(plot_path, transparent=False, bbox_inches='tight', pad_inches=0, dpi=300)
            if verbose:
                print("Save fig. in " + plot_path)
        plt.show()
        plt.close()
