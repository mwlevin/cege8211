"""Python version of ``dnl/node/Series.java``."""

from __future__ import annotations

from dnl.node.node import Node


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
        # if there is more than 1 upstream or downstream link, throw an error - this is not the intersection control you're looking for.
        if len(self.get_incoming()) != 1 or len(self.get_outgoing()) != 1:
            raise RuntimeError(f"Node {self.get_id()}: Wrong number of incoming or outgoing links: \n"
                               f"Incoming: {len(self.get_incoming())} Outgoing: {len(self.get_outgoing())}")

        us = self.get_incoming()[0]  # upstream link
        ds = self.get_outgoing()[0]  # downstream link

        y = min(us.get_sending_flow(), ds.get_receiving_flow())

        us.remove_flow(y)
        ds.add_flow(y)

    def update(self):
        # nothing to do here
        pass
