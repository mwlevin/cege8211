"""Python version of ``dnl/link/Link.java``."""

from __future__ import annotations

from abc import ABC, abstractmethod

from dnl.Params import Params


class Link(ABC):
    """A link in the network.

    This is an abstract class: key methods are not implemented, and must be
    implemented in subclasses. These depend on the specific flow model.
    """

    def __init__(self, id: int, source, dest, length: float, ffspd: float,
                 capacityPerLane: float, numLanes: int):
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
        :param capacityPerLane: capacity (per lane) in veh/hr
        :param numLanes: number of lanes
        """
        # store link parameters
        self.id = id
        self.source = source
        self.dest = dest
        self.capacityPerLane = capacityPerLane
        self.ffspd = ffspd
        self.length = length
        self.numLanes = numLanes

        # travel time information
        self.avgTT = 0.0
        self.totalFlow = 0.0

        # during each DNL, update total entering flow and total time spent occupying the link.
        self.total_time_occ = 0.0
        self.total_entering = 0.0

        # update incoming/outgoing sets of links in the Node class
        if source is not None:
            source.addLink(self)
        if dest is not None:
            dest.addLink(self)

    @abstractmethod
    def reset(self) -> None:
        """Resets this Link to start a new dynamic network loading."""

    def getFFSpeed(self) -> float:
        """Returns the free flow speed in mi/hr."""
        return self.ffspd

    def getFFTime(self) -> float:
        """Returns the free flow travel time in s."""
        return self.getLength() / self.getFFSpeed() * 3600.0

    def getAvgTT(self) -> float:
        """Returns the average travel time (in s) from the last dynamic network loading."""
        return max(self.avgTT, self.getFFTime())

    def getTotalTT(self) -> float:
        """Returns the total time spent traveling on this link (in s)."""
        return self.getAvgTT() * self.totalFlow

    def getAvgGrade(self) -> float:
        """Returns the average grade: vertical change in ft per horizontal distance in ft."""
        return (self.dest.getElevation() - self.source.getElevation()) / (self.getLength() * 5280)

    def getLength(self) -> float:
        """Returns the length in mi."""
        return self.length

    def getCapacityPerLane(self) -> float:
        """Returns the capacity per lane in veh/hr."""
        return self.capacityPerLane

    def getCapacity(self) -> float:
        """Returns the total capacity in veh/hr."""
        return self.capacityPerLane * self.numLanes

    def getNumLanes(self) -> float:
        """Returns the number of lanes."""
        return self.numLanes

    def getSource(self):
        """Returns the upstream Node for this Link."""
        return self.source

    def getDest(self):
        """Returns the downstream Node for this Link."""
        return self.dest

    def getId(self) -> int:
        """Returns the id for this Link."""
        return self.id

    @abstractmethod
    def getOccupancy(self) -> float:
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
    def addFlow(self, y: float) -> None:
        """Adds the given flow (in veh, for a single time step) to the upstream end of the link.

        This method is called when vehicles enter the link!
        This is usually called by the Node.step() method.
        Subclasses of Link need to call logEnteringFlow(y) to update the average travel times.
        """

    def logEnteringFlow(self, y: float) -> None:
        """Tracks the total number of vehicles entering this link.

        The number of vehicles is used to calculate the average travel time.
        Subclasses of Link should call this method as part of the addFlow() method.
        """
        self.total_entering += y

    def logOccupancyTime(self) -> None:
        """Used to calculate the average travel time. Called once per time step by the Network class."""
        self.total_time_occ += Params.dt * self.getOccupancy()

    def calculateTravelTime(self) -> None:
        """Calculates the travel time at the end of the dynamic network loading.

        The result can be accessed by getAvgTT(). This method is called in Network.simulate().
        """
        if self.total_entering > 0:
            self.avgTT = self.total_time_occ / self.total_entering
        else:
            self.avgTT = self.getFFTime()

        self.totalFlow = self.total_entering

        # now reset total_time_occ and total_entering for the next dynamic network loading.
        self.total_time_occ = 0.0
        self.total_entering = 0.0

    @abstractmethod
    def removeFlow(self, y: float) -> None:
        """Removes the given flow (in veh, for a single time step) from the downstream end of the link.

        This method is called when vehicles exit the link!
        This is usually called by the Node.step() method.
        """

    @abstractmethod
    def getSendingFlow(self) -> float:
        """Returns the maximum flow that could exit the link in the next time step (in veh)."""

    @abstractmethod
    def getReceivingFlow(self) -> float:
        """Returns the maximum flow that could enter the link in the next time step (in veh)."""

    def __lt__(self, other: "Link") -> bool:
        """Used to sort Links by id."""
        return self.id < other.id

    def __hash__(self) -> int:
        """Used for hashing. You can ignore it."""
        return self.id

    def __repr__(self) -> str:
        """Returns the id of this Link."""
        return str(self.id)
