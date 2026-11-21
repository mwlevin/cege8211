"""Python version of ``dnl/link/Cell.java``."""

from __future__ import annotations

from dnl.params import Params


class Cell:
    """A single cell in the cell transmission model.

    It should be constructed as needed by class CTM.
    """

    def __init__(self, link):
        """Constructs a Cell as part of the given CTM link.

        You may want to add additional parameters here.
        """
        # This is the CTM link that this cell belongs to. Having a reference is useful...
        self._link = link

        # Having references to the previous and next cell is probably useful for propagating flow.
        # These are initially None! You have to set these references in class CTM AFTER all the
        # cells have been constructed. Use set_next_cell(), set_prev_cell() to update these references.
        self._prev = None
        self._next = None

    def get_occupancy(self):
        # fill this in
        return 0.0

    def set_next_cell(self, next_cell):
        """Update the reference to the next (downstream) cell."""
        self._next = next_cell

    def set_prev_cell(self, prev_cell):
        """Update the reference to the previous (upstream) cell."""
        self._prev = prev_cell

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
