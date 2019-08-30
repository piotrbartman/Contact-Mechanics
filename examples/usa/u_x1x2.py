"""
Created at 21.08.2019

@author: Piotr Bartman
"""

import numpy as np
from simulation.simulation_runner import SimulationRunner
import numba


class Setup:
    gridHeight = 1
    cells_number = (20, 20)  # number of triangles per aside

    alpha = 18

    # f = lambda x1, x2, x3: x1+x2+x3
    # g = lambda x1, x2: 1
    b = 0
    rho = 1e-8

    @staticmethod
    def f(x1, x2):
        result = 0
        return result

    @staticmethod
    def g(x1, x2):
        if x1 == 1:
            result = x2
        if x2 == 1:
            result = x1
        return 0 * result

    @staticmethod
    @numba.jit()
    def regular_dphi(r, b, rho):
        x = r - b
        result = x / np.sqrt(x**2 + rho**2)
        return result


if __name__ == '__main__':
    setup = Setup()
    SimulationRunner.run(setup)
