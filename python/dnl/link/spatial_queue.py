"""Python version of ``dnl/link/SpatialQueue.java``."""

from __future__ import annotations

from dnl.link.point_queue import PointQueue
from dnl.params import Params


class SpatialQueue(PointQueue):
    """Propagates flow according to the spatial queue model.

    Includes capacity constraints and a density constraint per link.
    """

    def __init__(self, id, source, dest, length, ffspd, capacity_per_lane, num_lanes):
        super().__init__(id, source, dest, length, ffspd, capacity_per_lane, num_lanes)

    def get_receiving_flow(self):
        # fill this in
        return 0.0

    def add_flow(self, y):
        # fill this in
        pass

    def remove_flow(self, y):
        # fill this in
        pass

    def update(self):
        # fill this in
        pass
