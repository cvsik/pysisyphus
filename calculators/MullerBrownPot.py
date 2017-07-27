#!/usr/bin/env python3

import numpy as np

from calculators.Calculator import Calculator

class MullerBrownPot(Calculator):

    def __init__(self): 
        super(MullerBrownPot, self).__init__()


    def get_energy(self, atoms, coords):
        x, y, z = coords

        A  = (-200, -100, -170, 15)
        x0 = (1.0, 0.0, -0.5, -1.0)
        y0 = (0.0, 0.5, 1.5, 1.0)
        a  = (-1.0, -1.0, -6.5, 0.7)
        b  = (0.0, 0.0, 11.0, 0.6)
        c  = (-10.0, -10.0, -6.5, 0.7)

        energy = 0
        for i in range(4):
            energy += (A[i] * np.exp(
                        a[i] * (x - x0[i])**2 +
                        b[i] * (x - x0[i]) * (y - y0[i]) +
                        c[i] * (y - y0[i])**2
                      )
            )
        return {"energy": energy}

    def get_forces(self, atoms, coords):
        x, y, z = coords
        # https://www.wolframalpha.com/input/?i=derivative+of+(A*exp(a*(x-x0)**2+%2B+b*(x-x0)*(y-y0)+%2B+c*(y-y0)**2)
        A  = (-200, -100, -170, 15)
        x0 = (1.0, 0.0, -0.5, -1.0)
        y0 = (0.0, 0.5, 1.5, 1.0)
        a  = (-1.0, -1.0, -6.5, 0.7)
        b  = (0.0, 0.0, 11.0, 0.6)
        c  = (-10.0, -10.0, -6.5, 0.7)

        forces = 0
        dx = 0
        dy = 0
        for i in range(4):
            dx += (A[i] *
                    (2*a[i]*(x - x0[i]) + b[i]*(y - y0[i])) *
                    np.exp(
                        a[i] * (x - x0[i])**2 +
                        b[i] * (x - x0[i]) * (y - y0[i]) +
                        c[i] * (y - y0[i])**2
                    )
            )
            dy += (A[i] *
                    (b[i]*(x - x0[i]) + 2*c[i]*(y - y0[i])) *
                    np.exp(
                        a[i] * (x - x0[i])**2 +
                        b[i] * (x - x0[i]) * (y - y0[i]) +
                        c[i] * (y - y0[i])**2
                    )
            )
        dz = np.zeros_like(dx)
        forces = np.stack((dx, dy, dz), axis=-1)
        return {"forces": forces}

    """
    def get_hessian(self, atoms, coords):
        x, y, z = coords
        self._hessian = ((12*x**2 + 2 - 4*y, -4*x-2),
                         (-4*x-2, 4)
        )
    """

    def __str__(self):
        return "Müller-Brown-Potential"


if __name__ == "__main__":
    coords = (0.623, 0.028, 0)
    mbp = MullerBrownPot()
    atoms = ("H", )
    f=mbp.get_forces(atoms, coords)
    print(f)