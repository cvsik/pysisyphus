#!/usr/bin/env python3

import numpy as np

class Optimizer:

    def __init__(self, geometry, max_cycles=15):
        # https://stackoverflow.com/questions/5899185
        self.geometry = geometry

        self.max_cycles = max_cycles
        self.cur_cycle = 0

        self.max_force_thresh = 0.01
        self.rms_force_thresh = 0.001

        self.coords = list()

        self.forces = list()
        self.max_forces = list()
        self.rms_forces = list()

    def check_convergence(self, forces):
        max_force = forces.max()
        rms_force = np.sqrt(np.mean(np.square(forces)))

        self.max_forces.append(max_force)
        self.rms_forces.append(rms_force)

        print("cycle: {:03d} max(force): {: .5f} rms(force): {: .5f}".format(
            self.cur_cycle, max_force, rms_force)
        )

        return ((max_force <= self.max_force_thresh) and
                (rms_force <= self.rms_force_thresh)
        )

    def optimize(self):
        raise Exception("Not implemented!")

    def cycle(self):
        while self.cur_cycle < self.max_cycles:
            forces = self.geometry.forces
            self.forces.append(forces)
            self.coords.append(self.geometry.coords)
            if self.check_convergence(forces):
                break
            self.optimize()
            self.cur_cycle += 1