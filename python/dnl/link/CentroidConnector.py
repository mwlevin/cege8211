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

        # fill this in: add instance variables here

    def reset(self):
        # fill this in
        pass

    def getOccupancy(self):
        # fill this in
        return 0.0

    def step(self):
        # nothing to do here
        pass

    def update(self):
        # fill this in
        pass

    def getSendingFlow(self):
        # fill this in
        return 0.0

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
        # fill this in
        # INTEGER_MAX_VALUE can be used as a stand-in for infinity. Flow will never be that high.
        return 0.0

    def addFlow(self, y):
        # fill this in

        # keep this line: it records entering flow for travel time calculations
        self.logEnteringFlow(y)

    def removeFlow(self, y):
        # fill this in
        pass
