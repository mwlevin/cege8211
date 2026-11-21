"""Python version of ``dnl/node/Phase.java``."""

from __future__ import annotations


class Phase:
    """A single signal phase.

    It stores the green, yellow, and all-red times, as well as the permitted turning movements.
    """

    def __init__(self, green: float, yellow: float, red: float, turns_list):
        """:param turns_list: a list of (incoming link, outgoing link) pairs permitted during this phase."""
        self._red = red
        self._yellow = yellow
        self._green = green

        self._start_time = 0.0
        self._end_time = 0.0

        # maps each incoming link to the list of outgoing links it may turn onto during this phase
        self._turns = {}

        for (i, j) in turns_list:
            if i not in self._turns:
                self._turns[i] = []

            self._turns[i].append(j)

    def get_start_time(self) -> float:
        """Returns the exogenously specified start time of this phase."""
        return self._start_time

    def get_end_time(self) -> float:
        """Returns the exogenously specified end time of this phase."""
        return self._end_time

    def set_start_time(self, start: float) -> None:
        """Updates the start and end times given the specified start time.

        The end time is calculated based on the phase duration.
        """
        self._start_time = start
        self._end_time = self._start_time + self.get_duration()

    def get_duration(self) -> float:
        """Returns the duration of this phase, which is the sum of the green, yellow, and all-red time."""
        return self._red + self._yellow + self._green

    def get_green_duration(self, curr_time: float, end: float) -> float:
        """Returns the amount of green time if this phase were to be actuated from time curr_time to end.

        If the phase duration is too short, then a smaller green time will be returned.
        """
        end_green = self._start_time + self._green + self._yellow / 2

        return max(0, min(end, end_green) - curr_time)

    def get_turns(self) -> dict:
        """Returns a dict of turning movements permitted during this phase: incoming link -> list of outgoing links."""
        return self._turns
