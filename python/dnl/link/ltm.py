"""Python version of ``dnl/link/LTM.java``."""

from __future__ import annotations

import math
from collections import deque

from dnl.link.link import Link
from dnl.params import Params


class LTM(Link):
    """Propagates flow according to the link transmission model."""

    def __init__(self, id, source, dest, length, ffspd, capacity_per_lane, num_lanes):
        super().__init__(id, source, dest, length, ffspd, capacity_per_lane, num_lanes)

        self._yin = 0.0
        self._yout = 0.0

    def reset(self):
        # fill this in
        pass

    def get_occupancy(self):
        # fill this in
        return 0.0

    def step(self):
        # fill this in
        pass

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
