from __future__ import annotations

from dnl.node.Node import Node


class StopSign(Node):
    """The equal priority intersection discussed in class.

    Every approach has equal priority for intersection flow.
    """

    def __init__(self, id, longitude, latitude, elevation):
        super().__init__(id, longitude, latitude, elevation)

    def reset(self):
        # fill this in
        pass

    def step(self):
        # fill this in
        pass

    def update(self):
        # fill this in
        pass
