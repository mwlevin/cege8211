from __future__ import annotations

from dnl.node.Node import Node


class Series(Node):
    """Connects two links, possibly with different capacities.

    The behavior is to move vehicles given by min(sending flow, receiving flow).
    """

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)

    def reset(self):
        # nothing to do here
        pass

    def step(self):
        # move flow from upstream link to downstream link as permitted by sending and receiving flows.
        # if there is more than 1 upstream or downstream link, raise an error - this is not the intersection control you're looking for.
        if len(self.getIncoming()) != 1 or len(self.getOutgoing()) != 1:
            raise RuntimeError(f"Node {self.getId()}: Wrong number of incoming or outgoing links: \n"
                               f"Incoming: {len(self.getIncoming())} Outgoing: {len(self.getOutgoing())}")

        us = self.getIncoming()[0]  # upstream link
        ds = self.getOutgoing()[0]  # downstream link

        y = min(us.getSendingFlow(), ds.getReceivingFlow())

        us.removeFlow(y)
        ds.addFlow(y)

    def update(self):
        # nothing to do here
        pass
