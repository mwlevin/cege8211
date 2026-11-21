from __future__ import annotations

from dnl.node.Node import Node
from dnl.Params import Params


class PedSignal(Node):
    """Two links in series, separated by a traffic light used to provide access to pedestrians.

    Essentially, the light alternates between green and red, with these times as class parameters.
    The primary utility of this class is to create a simple signal that can cause congestion waves to form.
    """

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)

        # change these to modify the green time and red time.
        # I assume that the time step is less than the cycle length.
        self.green_time = 32
        self.red_time = 15

        # alternate green and red, then cycle back when needed
        self.curr_time = 0.0
        self.cycle_length = self.green_time + self.red_time

    def reset(self):
        self.curr_time = 0.0

    def step(self):
        green_time = self.green_time
        cycle_length = self.cycle_length
        green_dt = 0.0

        # assume that time step is less than the cycle length
        start_time = self.curr_time
        end_time = self.curr_time + Params.dt

        # check green phase
        time_rem = min(max(0, green_time - start_time), end_time - start_time)
        green_dt += time_rem
        start_time += time_rem

        time_rem = min(max(0, cycle_length - start_time), end_time - start_time)
        start_time += time_rem

        time_rem = min(max(0, green_time + cycle_length - start_time), end_time - start_time)
        green_dt += time_rem
        start_time += time_rem

        self.curr_time = end_time
        if self.curr_time >= cycle_length:
            self.curr_time -= cycle_length

        us = self.getIncoming()[0]
        ds = self.getOutgoing()[0]

        y = min(us.getSendingFlow(), ds.getReceivingFlow()) * green_dt / Params.dt

        us.removeFlow(y)
        ds.addFlow(y)

    def update(self):
        pass
