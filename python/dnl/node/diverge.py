"""Python version of ``dnl/node/Diverge.java``."""

from __future__ import annotations

from dnl.node.node import Node
from dnl.params import Params


class Diverge(Node):
    """A diverge: where 1 upstream link branches out into 2 or more downstream links."""

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
