"""Python version of ``dnl/link/MN.java``."""

from __future__ import annotations

from dnl.link.link import Link
from dnl.params import Params, INTEGER_MAX_VALUE


class MN(Link):

    def __init__(self, id, source, dest, length, ffspd, capacity_per_lane, num_lanes):
        super().__init__(id, source, dest, length, ffspd, capacity_per_lane, num_lanes)

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
