"""Python version of ``dnl/node/PedSignal.java``."""

from __future__ import annotations

from dnl.node.node import Node
from dnl.params import Params


class PedSignal(Node):
    """Two links in series, separated by a traffic light used to provide access to pedestrians.

    Essentially, the light alternates between green and red, with these times as class parameters.
    The primary utility of this class is to create a simple signal that can cause congestion waves to form.
    """

    # change these to modify the green time and red time.
    # I assume that the time step is less than the cycle length.
    GREEN_TIME = 32
    RED_TIME = 15

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)

        # alternate green and red, then cycle back when needed
        self._cycle_length = self.GREEN_TIME + self.RED_TIME
        self._curr_time = 0.0

    def reset(self):
        self._curr_time = 0.0

    def step(self):
        green_time = self.GREEN_TIME
        cycle_length = self._cycle_length
        green_dt = 0.0

        # assume that time step is less than the cycle length
        start_time = self._curr_time
        end_time = self._curr_time + Params.dt

        # check green phase
        time_rem = min(max(0, green_time - start_time), end_time - start_time)
        green_dt += time_rem
        start_time += time_rem

        time_rem = min(max(0, cycle_length - start_time), end_time - start_time)
        start_time += time_rem

        time_rem = min(max(0, green_time + cycle_length - start_time), end_time - start_time)
        green_dt += time_rem
        start_time += time_rem

        self._curr_time = end_time
        if self._curr_time >= cycle_length:
            self._curr_time -= cycle_length

        us = self.get_incoming()[0]
        ds = self.get_outgoing()[0]

        y = min(us.get_sending_flow(), ds.get_receiving_flow()) * green_dt / Params.dt

        us.remove_flow(y)
        ds.add_flow(y)

    def update(self):
        pass
