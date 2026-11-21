from __future__ import annotations

import math
from collections import deque

from dnl.link.Link import Link
from dnl.Params import Params


class PointQueue(Link):
    """Propagates flow according to the point queue model (no spatial constraints)."""

    def __init__(self, id, source, dest, length, ffspd, capacityPerLane, numLanes):
        super().__init__(id, source, dest, length, ffspd, capacityPerLane, numLanes)

    def reset(self):
        # fill this in
        pass

    def getOccupancy(self):
        # fill this in
        return 0.0

    def step(self):
        # fill this in
        pass

    def update(self):
        # fill this in
        pass

    def getSendingFlow(self):
        # fill this in
        return 0.0

    def getReceivingFlow(self):
        # fill this in
        return 0.0

    def addFlow(self, y):
        # fill this in
        pass

    def removeFlow(self, y):
        # fill this in
        pass
