"""Global parameters that are useful across the entire project.

The values are stored as class attributes of :class:`Params`, so every module
sees the same values. Always access them through the class, e.g.
``Params.dt`` or ``Params.time``.
"""

import sys
from pathlib import Path


class Params:
    """Stores important global parameters that are useful across the entire project."""

    dt = 6
    """The time step, in seconds."""

    time = 0
    """The current time in the network (s). Updated when Network.nextTimestep() is called."""

    DURATION = 7200
    """The end time of the simulation, in s. The maximum number of time steps is DURATION/dt."""

    JAM_DENSITY = 264.0
    """The exogenous jam density, in veh/mi/lane."""


# Folder that contains the networks/ folder, the HW*.txt files, and log.txt.
# This is the "python" folder, so the code works no matter which directory you run it from.
BASE_DIR = Path(__file__).resolve().parent.parent

# Stand-ins for "infinity". Flow will never be this high.
INTEGER_MAX_VALUE = 2147483647
DOUBLE_MAX_VALUE = sys.float_info.max
