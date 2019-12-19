#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pytest

from pysisyphus.calculators.AnaPot import AnaPot
from pysisyphus.calculators.PySCF import PySCF
from pysisyphus.calculators.Gaussian16 import Gaussian16
from pysisyphus.constants import BOHR2ANG
from pysisyphus.helpers import geom_from_library
from pysisyphus.irc import *
from pysisyphus.testing import using


def plot_irc(irc, title=None):
    geom = irc.geometry
    calc = geom.calculator
    calc.plot()
    ax = calc.ax
    ax.plot(*irc.all_coords.T[:2], "ro-")
    if title:
        ax.set_title(title)
    plt.show()


@pytest.mark.parametrize(
    "irc_cls, mod_kwargs, ref", [
        (DampedVelocityVerlet, {"v0": 0.1, "max_cycles": 400,}, None),
        (Euler, {"step_length": 0.05,}, None),
        (EulerPC, {}, None),
        (GonzalesSchlegel, {}, None),
        (IMKMod, {}, None),
        (RK4, {}, None),
        (LQA, {}, None),
    ]
)
def test_anapot_irc(irc_cls, mod_kwargs, ref):
    geom = AnaPot().get_geom((0.61173, 1.49297, 0.))

    kwargs = {
        "step_length": 0.1,
        "rms_grad_thresh": 1e-2,
    }
    kwargs.update(**mod_kwargs)

    irc = irc_cls(geom, **kwargs)
    irc.run()

    fc = irc.all_coords[0]
    bc = irc.all_coords[-1]
    forward_ref = np.array((-1.0527, 1.0278,  0.))
    backward_ref = np.array((1.941, 3.8543, 0.))
    forward_diff = np.linalg.norm(fc - forward_ref)
    backward_diff = np.linalg.norm(bc - backward_ref)
    assert forward_diff == pytest.approx(0.05, abs=0.1)
    assert backward_diff == pytest.approx(0.05, abs=0.1)

    # plot_irc(irc, irc.__class__.__name__)


@pytest.mark.parametrize(
    "calc_cls, kwargs_", [
        pytest.param(PySCF, {"basis": "321g", }, marks=using("pyscf")),
        pytest.param(Gaussian16, {"route": "HF/3-21G"}, marks=using("gaussian16")),
    ]
)
def test_hf_abstraction_dvv(calc_cls, kwargs_):
    geom = geom_from_library("hfabstraction_hf321g_displ_forward.xyz")

    calc_kwargs = {
        "pal": 2,
    }
    calc_kwargs.update(kwargs_)

    print("Using", calc_cls)
    calc = calc_cls(**calc_kwargs)
    geom.set_calculator(calc)

    irc_kwargs = {
        "dt0": 0.5,
        "v0": 0.04,
        "downhill": True,
    }
    dvv = DampedVelocityVerlet(geom, **irc_kwargs)
    dvv.run()

    c3d = geom.coords3d * BOHR2ANG
    def bond(i,j): return np.linalg.norm(c3d[i]-c3d[j])

    assert bond(2, 7) == pytest.approx(0.93, abs=0.01)
    assert bond(4, 7) == pytest.approx(2.42, abs=0.01)
    assert bond(2, 0) == pytest.approx(2.23, abs=0.01)