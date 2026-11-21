"""Python version of ``dnl/node/Sink.java``."""

from __future__ import annotations

from dnl.node.node import Node


class Sink(Node):
    """Behavior at a sink (destination node): all vehicles reaching the sink are removed from the network."""

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)
        self._exiting = 0.0

    def reset(self):
        self._exiting = 0.0

    def step(self):
        self._exiting = 0.0
        # all vehicles reaching the sink are removed.
        for us in self.get_incoming():
            y = us.get_sending_flow()
            self._exiting += y
            us.remove_flow(y)

    def update(self):
        # nothing to do here
        pass

    def get_num_exiting(self) -> float:
        return self._exiting

    def store_turning_proportion(self, i, j, p):
        # removed due to uselessness
        pass

    def get_turning_prop(self, i, j):
        # all vehicles exit when reaching the sink
        return 1
