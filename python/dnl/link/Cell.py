"""Python version of ``dnl/link/Cell.java``."""

from __future__ import annotations

from dnl.Params import Params


class Cell:
    """A single cell in the cell transmission model.

    It should be constructed as needed by class CTM.
    """

    def __init__(self, link):
        """Constructs a Cell as part of the given CTM link.

        You may want to add additional parameters here.
        """
        # This is the CTM link that this cell belongs to. Having a reference is useful...
        self.link = link

        # Having references to the previous and next cell is probably useful for propagating flow.
        # These are initially None! You have to set these references in class CTM AFTER all the
        # cells have been constructed. Use setNextCell(), setPrevCell() to update these references.
        self.prev = None
        self.next = None

    def getOccupancy(self):
        # fill this in
        return 0.0

    def setNextCell(self, next):
        """Update the reference to the next (downstream) cell."""
        self.next = next

    def setPrevCell(self, prev):
        """Update the reference to the previous (upstream) cell."""
        self.prev = prev

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
