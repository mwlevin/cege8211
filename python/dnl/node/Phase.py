"""Python version of ``dnl/node/Phase.java``."""

from __future__ import annotations


class Phase:
    """A single signal phase.

    It stores the green, yellow, and all-red times, as well as the permitted turning movements.
    """

    def __init__(self, green: float, yellow: float, red: float, turnslist):
        """:param turnslist: a list of (incoming link, outgoing link) pairs permitted during this phase."""
        self.red = red
        self.yellow = yellow
        self.green = green

        self.start_time = 0.0
        self.end_time = 0.0

        # maps each incoming link to the list of outgoing links it may turn onto during this phase
        self.turns = {}

        for (i, j) in turnslist:
            if i not in self.turns:
                self.turns[i] = []

            self.turns[i].append(j)

    def getStartTime(self) -> float:
        """Returns the exogenously specified start time of this phase."""
        return self.start_time

    def getEndTime(self) -> float:
        """Returns the exogenously specified end time of this phase."""
        return self.end_time

    def setStartTime(self, start: float) -> None:
        """Updates the start and end times given the specified start time.

        The end time is calculated based on the phase duration.
        """
        self.start_time = start
        self.end_time = self.start_time + self.getDuration()

    def getDuration(self) -> float:
        """Returns the duration of this phase, which is the sum of the green, yellow, and all-red time."""
        return self.red + self.yellow + self.green

    def getGreenDuration(self, curr_time: float, end: float) -> float:
        """Returns the amount of green time if this phase were to be actuated from time curr_time to end.

        If the phase duration is too short, then a smaller green time will be returned.
        """
        end_green = self.start_time + self.green + self.yellow / 2

        return max(0, min(end, end_green) - curr_time)

    def getTurns(self) -> dict:
        """Returns a dict of turning movements permitted during this phase: incoming link -> list of outgoing links."""
        return self.turns
