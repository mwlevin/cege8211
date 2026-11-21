"""Python version of ``dnl/node/Source.java``."""

from __future__ import annotations

from dnl.link.link import Link
from dnl.node.node import Node
from dnl.params import Params


class _DummyLink(Link):
    """A placeholder link that serves as the "incoming link" of a Source, since a source has no incoming links."""

    def __init__(self):
        super().__init__(-1, None, None, 0, 0, 0, 0)

    def reset(self): pass
    def step(self): pass
    def update(self): pass
    def get_sending_flow(self): return 0
    def get_receiving_flow(self): return 0
    def add_flow(self, y): pass
    def remove_flow(self, y): pass
    def get_occupancy(self): return 0


class Source(Node):
    """A source (origin node): vehicles spawn at this location at predetermined rates."""

    def __init__(self, id, longitude, latitude, elevation):
        """See the Node constructor."""
        super().__init__(id, longitude, latitude, elevation)

        # This stores the rate of demand as a list of (start time, end time, rate) entries.
        # For instance, the entry (0, 20, 50) means that when the time is between 0 and 20s, 50veh/hr enter at this source.
        self._demand_rates = []

        # This is actually useful - it stores which downstream link entering vehicles go to!
        # We need a dummy link to serve as the incoming link, since a source does not have incoming links.
        self._dummy = _DummyLink()

    def reset(self):
        # nothing to do here
        pass

    def add_demand(self, start_time: float, end_time: float, demand: float) -> None:
        """Adds demand to the source. It is typically called in ReadNetwork when constructing the Network."""
        self._demand_rates.append((start_time, end_time, demand))

    def get_total_demand(self, start_time: float, end_time: float) -> float:
        """Returns the total demand that enters the network between the two times."""
        output = 0.0

        for (t0, t1, rate) in self._demand_rates:
            start = max(start_time, t0)
            end = min(end_time, t1)

            output += rate * (end - start) / 3600.0

        return output

    def step(self):
        """Called every time step by Network.next_timestep().

        Since this is a source node, it adds the exogenous amount of demand to the
        network - to the appropriate CentroidConnector.
        """
        # Here we need to add the specified amount of demand to the network.
        # First, calculate the rate at which vehicles enter during the next time step.
        # The time interval is [Params.time, Params.time + Params.dt).
        # If the demand applies for part of the time interval, scale the rate proportionally to the overlap.
        rate = 0.0

        for (t0, t1, demand) in self._demand_rates:
            start_time = max(Params.time, t0)
            end_time = min(Params.time + Params.dt, t1)

            if end_time >= start_time:
                rate += demand * (end_time - start_time) / 3600.0

        # now add demand at the given rate
        new_demand = rate

        # split it according to turning proportions
        for ds in self.get_outgoing():
            ds.add_flow(new_demand * self.get_turning_prop(None, ds))

    def update(self):
        # nothing to do here
        pass

    def store_turning_proportion(self, i, j, p):
        """Used to store exogenous turning proportions from input data."""
        super().store_turning_proportion(self._dummy, j, p)

    def get_turning_prop(self, i, j):
        """Returns the proportion of vehicles turning from Link i to Link j."""
        return super().get_turning_prop(self._dummy, j)
