"""Python version of ``dnl/link/CTM.java``."""

from __future__ import annotations

import math

from dnl.link.Cell import Cell
from dnl.link.Link import Link
from dnl.Params import Params


class CTM(Link):
    """Propagates flow according to the cell transmission model."""

    def __init__(self, id, source, dest, length, ffspd, capacityPerLane, numLanes):
        super().__init__(id, source, dest, length, ffspd, capacityPerLane, numLanes)

        # This is the list of cells used to model this link.
        # It is empty! You need to create the cells here.
        # Note: Python's round() rounds halves to the nearest even number (round(2.5) == 2).
        # To round halves up like Java's Math.round(), use int(math.floor(x + 0.5)).
        self.cells = []

    def reset(self):
        # fill this in
        pass

    def getCellLength(self):
        return 0.0

    def step(self):
        # fill this in
        pass

    def getOccupancy(self):
        # fill this in
        return 0.0

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

    def getFFTime(self):
        return len(self.cells) * Params.dt
