"""Python version of ``dnl/link/CTM.java``."""

from __future__ import annotations

import math

from dnl.link.cell import Cell
from dnl.link.link import Link
from dnl.params import Params


class CTM(Link):
    """Propagates flow according to the cell transmission model."""

    def __init__(self, id, source, dest, length, ffspd, capacity_per_lane, num_lanes):
        super().__init__(id, source, dest, length, ffspd, capacity_per_lane, num_lanes)

        # This is the list of cells used to model this link.
        # It is empty! You need to create the cells here.
        # Note: Python's round() rounds halves to the nearest even number (round(2.5) == 2).
        # To round halves up like Java's Math.round(), use int(math.floor(x + 0.5)).
        self._cells = []

    def reset(self):
        # fill this in
        pass

    def get_cell_length(self):
        return 0.0

    def step(self):
        # fill this in
        pass

    def get_occupancy(self):
        # fill this in
        return 0.0

    def update(self):
        # fill this in
        pass

    def get_sending_flow(self):
        # fill this in
        return 0.0

    def get_receiving_flow(self):
        # fill this in
        return 0.0

    def add_flow(self, y):
        # fill this in
        pass

    def remove_flow(self, y):
        # fill this in
        pass

    def get_ff_time(self):
        return len(self._cells) * Params.dt
