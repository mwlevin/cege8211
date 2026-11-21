"""Python version of ``dnl/link/Link.java``."""

from __future__ import annotations

from abc import ABC, abstractmethod

from dnl.params import Params


class Link(ABC):
    """A link in the network.

    This is an abstract class: key methods are not implemented, and must be
    implemented in subclasses. These depend on the specific flow model.
    """

    def __init__(self, id: int, source, dest, length: float, ffspd: float,
                 capacity_per_lane: float, num_lanes: int):
        """Constructs a new Link with the given parameters.

        Generally Links will be constructed in ReadNetwork.
        Jam density is global and found in Params.
        Backwards wave speed may or may not be calculated based on these
        parameters - depends on the flow model.

        :param id: id of this Link
        :param source: start Node of this Link
        :param dest: end Node of this Link
        :param length: length in mi
        :param ffspd: free flow speed in mi/hr
        :param capacity_per_lane: capacity (per lane) in veh/hr
        :param num_lanes: number of lanes
        """
        # store link parameters
        self._id = id
        self._source = source
        self._dest = dest
        self._capacity_per_lane = capacity_per_lane
        self._ffspd = ffspd
        self._length = length
        self._num_lanes = num_lanes

        # travel time information
        self._avg_tt = 0.0
        self._total_flow = 0.0

        # during each DNL, update total entering flow and total time spent occupying the link.
        self._total_time_occ = 0.0
        self._total_entering = 0.0

        # update incoming/outgoing sets of links in the Node class
        if source is not None:
            source.add_link(self)
        if dest is not None:
            dest.add_link(self)

    @abstractmethod
    def reset(self) -> None:
        """Resets this Link to start a new dynamic network loading."""

    def get_ff_speed(self) -> float:
        """Returns the free flow speed in mi/hr."""
        return self._ffspd

    def get_ff_time(self) -> float:
        """Returns the free flow travel time in s."""
        return self.get_length() / self.get_ff_speed() * 3600.0

    def get_avg_tt(self) -> float:
        """Returns the average travel time (in s) from the last dynamic network loading."""
        return max(self._avg_tt, self.get_ff_time())

    def get_total_tt(self) -> float:
        """Returns the total time spent traveling on this link (in s)."""
        return self.get_avg_tt() * self._total_flow

    def get_avg_grade(self) -> float:
        """Returns the average grade: vertical change in ft per horizontal distance in ft."""
        return (self._dest.get_elevation() - self._source.get_elevation()) / (self.get_length() * 5280)

    def get_length(self) -> float:
        """Returns the length in mi."""
        return self._length

    def get_capacity_per_lane(self) -> float:
        """Returns the capacity per lane in veh/hr."""
        return self._capacity_per_lane

    def get_capacity(self) -> float:
        """Returns the total capacity in veh/hr."""
        return self._capacity_per_lane * self._num_lanes

    def get_num_lanes(self) -> float:
        """Returns the number of lanes."""
        return self._num_lanes

    def get_source(self):
        """Returns the upstream Node for this Link."""
        return self._source

    def get_dest(self):
        """Returns the downstream Node for this Link."""
        return self._dest

    def get_id(self) -> int:
        """Returns the id for this Link."""
        return self._id

    @abstractmethod
    def get_occupancy(self) -> float:
        """Returns the number of vehicles currently on this Link."""

    @abstractmethod
    def step(self) -> None:
        """Called every time step. For the Link class, step() should propagate flow along the link."""

    @abstractmethod
    def update(self) -> None:
        """Called every time step, after step() has been called for all Nodes and Links.

        It can be used to finish any updating work that could not occur during step().
        """

    @abstractmethod
    def add_flow(self, y: float) -> None:
        """Adds the given flow (in veh, for a single time step) to the upstream end of the link.

        This method is called when vehicles enter the link!
        This is usually called by the Node.step() method.
        Subclasses of Link need to call log_entering_flow(y) to update the average travel times.
        """

    def log_entering_flow(self, y: float) -> None:
        """Tracks the total number of vehicles entering this link.

        The number of vehicles is used to calculate the average travel time.
        Subclasses of Link should call this method as part of the add_flow() method.
        """
        self._total_entering += y

    def log_occupancy_time(self) -> None:
        """Used to calculate the average travel time. Called once per time step by the Network class."""
        self._total_time_occ += Params.dt * self.get_occupancy()

    def calculate_travel_time(self) -> None:
        """Calculates the travel time at the end of the dynamic network loading.

        The result can be accessed by get_avg_tt(). This method is called in Network.simulate().
        """
        if self._total_entering > 0:
            self._avg_tt = self._total_time_occ / self._total_entering
        else:
            self._avg_tt = self.get_ff_time()

        self._total_flow = self._total_entering

        # now reset total_time_occ and total_entering for the next dynamic network loading.
        self._total_time_occ = 0.0
        self._total_entering = 0.0

    @abstractmethod
    def remove_flow(self, y: float) -> None:
        """Removes the given flow (in veh, for a single time step) from the downstream end of the link.

        This method is called when vehicles exit the link!
        This is usually called by the Node.step() method.
        """

    @abstractmethod
    def get_sending_flow(self) -> float:
        """Returns the maximum flow that could exit the link in the next time step (in veh)."""

    @abstractmethod
    def get_receiving_flow(self) -> float:
        """Returns the maximum flow that could enter the link in the next time step (in veh)."""

    def __lt__(self, other: "Link") -> bool:
        """Used to sort Links by id."""
        return self._id < other._id

    def __hash__(self) -> int:
        """Used for hashing. You can ignore it."""
        return self._id

    def __repr__(self) -> str:
        """Returns the id of this Link."""
        return str(self._id)
