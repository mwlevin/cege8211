"""Python version of ``dnl/Path.java``."""

from __future__ import annotations


class Path(list):
    """A path, which is an ordered list of Links. It is constructed as a subclass of list."""

    def getFFTime(self) -> float:
        """Returns the free flow travel time of this path in s."""
        output = 0.0
        for link in self:
            output += link.getFFTime()
        return output

    def getAvgTime(self) -> float:
        """Returns the average travel time of this path in s."""
        output = 0.0
        for link in self:
            output += link.getAvgTT()
        return output

    def getLength(self) -> float:
        """Returns the total length of this path in mi."""
        output = 0.0
        for link in self:
            output += link.getLength()
        return output
