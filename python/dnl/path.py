"""Python version of ``dnl/Path.java``."""

from __future__ import annotations


class Path(list):
    """A path, which is an ordered list of Links. It is constructed as a subclass of list."""

    def get_ff_time(self) -> float:
        """Returns the free flow travel time of this path in s."""
        output = 0.0
        for link in self:
            output += link.get_ff_time()
        return output

    def get_avg_time(self) -> float:
        """Returns the average travel time of this path in s."""
        output = 0.0
        for link in self:
            output += link.get_avg_tt()
        return output

    def get_length(self) -> float:
        """Returns the total length of this path in mi."""
        output = 0.0
        for link in self:
            output += link.get_length()
        return output
