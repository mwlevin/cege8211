"""Python version of ``dnl/node/Sink.java``."""

from __future__ import annotations

from dnl.node.Node import Node


class Sink(Node):
    """Behavior at a sink (destination node): all vehicles reaching the sink are removed from the network."""

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)
        self.exiting = 0.0

    def reset(self):
        self.exiting = 0.0

    def step(self):
        self.exiting = 0.0
        # all vehicles reaching the sink are removed.
        for us in self.getIncoming():
            y = us.getSendingFlow()
            self.exiting += y
            us.removeFlow(y)

    def update(self):
        # nothing to do here
        pass

    def getNumExiting(self) -> float:
        return self.exiting

    def storeTurningProportion(self, i, j, p):
        # removed due to uselessness
        pass

    def getTurningProp(self, i, j):
        # all vehicles exit when reaching the sink
        return 1
