"""Python version of ``dnl/link/SpatialQueue.java``."""

from __future__ import annotations

from dnl.link.PointQueue import PointQueue
from dnl.Params import Params


class SpatialQueue(PointQueue):
    """Propagates flow according to the spatial queue model.

    Includes capacity constraints and a density constraint per link.
    """

    def __init__(self, id, source, dest, length, ffspd, capacityPerLane, numLanes):
        super().__init__(id, source, dest, length, ffspd, capacityPerLane, numLanes)

    def getReceivingFlow(self):
        # fill this in
        return 0.0

    def addFlow(self, y):
        # fill this in
        pass

    def removeFlow(self, y):
        # fill this in
        pass

    def update(self):
        # fill this in
        pass
