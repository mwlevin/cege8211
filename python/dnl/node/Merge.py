from __future__ import annotations

from dnl.node.Node import Node
from dnl.Params import Params


class Merge(Node):
    """A merge: where 2 or more upstream links combine into 1 downstream link."""

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
