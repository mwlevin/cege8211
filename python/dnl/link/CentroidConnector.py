from __future__ import annotations

from dnl.link.Link import Link
from dnl.Params import Params, INTEGER_MAX_VALUE, DOUBLE_MAX_VALUE


class CentroidConnector(Link):
    """A centroid connector (no capacity constraint, no density constraint).

    Centroid connectors are typically used as a buffer zone between sources/sinks and the main network.
    """

    def __init__(self, id, source, dest, length, ffspd, capacityPerLane, numLanes):
        # these values actually don't matter!
        super().__init__(id, source, dest, 1, 60, 100000, 1)

        # store the occupancy: that is the sending flow also.
        self.n = 0.0

        # this will be the change in occupancy at the next time step
        self.total_y = 0.0

    def reset(self):
        self.n = 0.0
        self.total_y = 0.0

    def getOccupancy(self):
        return self.n

    def step(self):
        # nothing to do here
        pass

    def update(self):
        # addFlow() and removeFlow() updated total_y; now we need to propagate those changes to the occupancy
        self.n = max(0, self.n + self.total_y)

        # zero out total_y for the next time step
        self.total_y = 0.0

    def getSendingFlow(self):
        # all flow can exit
        return self.n

    def getFFTime(self):
        """Returns the free flow travel time in s."""
        return Params.dt

    def getCapacityPerLane(self):
        """Returns the capacity per lane in veh/hr."""
        return DOUBLE_MAX_VALUE

    def getCapacity(self):
        """Returns the total capacity in veh/hr."""
        return DOUBLE_MAX_VALUE

    def getReceivingFlow(self):
        # no constraint on entering flow
        # I'm using INTEGER_MAX_VALUE as a stand-in for infinity. Flow will never be that high.
        return INTEGER_MAX_VALUE

    def addFlow(self, y):
        # add y to the occupancy for the next time step
        self.total_y += y
        self.logEnteringFlow(y)

    def removeFlow(self, y):
        # remove y from the occupancy for the next time step
        self.total_y -= y
