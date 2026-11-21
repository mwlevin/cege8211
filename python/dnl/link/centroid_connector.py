"""Python version of ``dnl/link/CentroidConnector.java``."""

from __future__ import annotations

from dnl.link.link import Link
from dnl.params import Params, INTEGER_MAX_VALUE, DOUBLE_MAX_VALUE


class CentroidConnector(Link):
    """A centroid connector (no capacity constraint, no density constraint).

    Centroid connectors are typically used as a buffer zone between sources/sinks and the main network.
    """

    def __init__(self, id, source, dest, length, ffspd, capacity_per_lane, num_lanes):
        # these values actually don't matter!
        super().__init__(id, source, dest, 1, 60, 100000, 1)

        # store the occupancy: that is the sending flow also.
        self._n = 0.0

        # this will be the change in occupancy at the next time step
        self._total_y = 0.0

    def reset(self):
        self._n = 0.0
        self._total_y = 0.0

    def get_occupancy(self):
        return self._n

    def step(self):
        # nothing to do here
        pass

    def update(self):
        # add_flow() and remove_flow() updated total_y; now we need to propagate those changes to the occupancy
        self._n = max(0, self._n + self._total_y)

        # zero out total_y for the next time step
        self._total_y = 0.0

    def get_sending_flow(self):
        # all flow can exit
        return self._n

    def get_ff_time(self):
        """Returns the free flow travel time in s."""
        return Params.dt

    def get_capacity_per_lane(self):
        """Returns the capacity per lane in veh/hr."""
        return DOUBLE_MAX_VALUE

    def get_capacity(self):
        """Returns the total capacity in veh/hr."""
        return DOUBLE_MAX_VALUE

    def get_receiving_flow(self):
        # no constraint on entering flow
        # I'm using INTEGER_MAX_VALUE as a stand-in for infinity. Flow will never be that high.
        return INTEGER_MAX_VALUE

    def add_flow(self, y):
        # add y to the occupancy for the next time step
        self._total_y += y
        self.log_entering_flow(y)

    def remove_flow(self, y):
        # remove y from the occupancy for the next time step
        self._total_y -= y
