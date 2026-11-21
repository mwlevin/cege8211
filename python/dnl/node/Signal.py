from __future__ import annotations

from dnl.node.Node import Node
from dnl.node.Phase import Phase
from dnl.Params import Params


class Signal(Node):
    """A traffic signal. There can be any number of incoming and outgoing links.

    During construction, addPhase() and setOffset() will be called to store signal cycle information.
    addPhase() adds a phase to the signal cycle; setOffset() sets the start time of the cycle (relative to 0).
    """

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)

        self.phases = []
        self.offset = 0.0

        self.curr_phase = -1
        self.cycle_length = 0.0

        # this is the time in the cycle. It resets to 0 whenever the cycle duration is exceeded.
        self.curr_time = 0.0

    def reset(self):
        # fill this in
        pass

    def step(self):
        """Use a diverge node to model outgoing flow for each approach."""
        # fill this in
        pass

    def update(self):
        # fill this in
        pass

    def getCycleLength(self) -> float:
        """Returns the length of the cycle, in s."""
        return self.cycle_length

    def setOffset(self, offset: float) -> None:
        """Updates the offset of the signal cycle (in s).

        For instance, if the offset is 21s, then phase 1 starts at t=21s.
        Note that the signal cycle repeats, so there will always be a phase active at t=0.
        Depending on the offset, it may not be the first phase!
        """
        self.offset = offset

    def addPhase(self, sequence: int, green: float, yellow: float, all_red: float, protected_turns) -> None:
        """Adds the specified phase to this signal. Recall that a signal cycle consists of a list of phases.

        Sequence is the order that this phase occurs in a fixed cycle, starting from 1.
        Green, yellow, and all-red time are in seconds.
        protected_turns is a list of (incoming link, outgoing link) pairs.
        For instance, if (i, j) is in protected_turns, then this phase allows movement from i to j.
        """
        phase = Phase(green, yellow, all_red, protected_turns)
        self.phases.insert(sequence - 1, phase)
        self.cycle_length += phase.getDuration()
