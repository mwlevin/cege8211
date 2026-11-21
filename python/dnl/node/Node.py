"""Python version of ``dnl/node/Node.java``."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Node(ABC):
    """A node in the network.

    This is an abstract class: key methods are not implemented, and must be
    implemented in subclasses. These depend on the specific intersection model.
    """

    def __init__(self, id: int, longitude: float, latitude: float, elevation: float):
        """Constructs the Node with the given id, longitude, latitude, and elevation.

        The incoming and outgoing lists of Links will be updated automatically as Links are constructed.

        :param id: the id of this Node
        :param longitude: the longitude portion of the location
        :param latitude: the latitude portion of the location
        :param elevation: the elevation (in ft)
        """
        # store node parameters
        self.id = id
        self.elevation = elevation
        self.latitude = latitude
        self.longitude = longitude

        # construct incoming and outgoing lists. They will be populated as links are constructed.
        self.incoming = []
        self.outgoing = []

        # Stores turning proportions between links: turning_prop[i][j] is the proportion from link i to link j.
        # Turning proportions specify the route assignment.
        self.turning_prop = {}

        # used by shortest path
        self.pred = None
        self.cost = 0.0

    @abstractmethod
    def reset(self) -> None:
        """Resets this Node to start a new dynamic network loading."""

    def getElevation(self) -> float:
        """Returns the elevation (in ft)."""
        return self.elevation

    def getLatitude(self) -> float:
        """Returns the latitude."""
        return self.latitude

    def getLongitude(self) -> float:
        """Returns the longitude."""
        return self.longitude

    def storeTurningProportion(self, i, j, p: float) -> None:
        """Used when constructing the Node: adjusts the turning proportion from Link i to Link j.

        Turning proportions must add to 1 for all incoming Links.
        """
        if i not in self.turning_prop:
            self.turning_prop[i] = {}
        self.turning_prop[i][j] = p

    def getTurningProportions(self) -> dict:
        """Returns the dict of turning proportions."""
        return self.turning_prop

    def clearTurningProportions(self) -> None:
        """Deletes all stored turning proportions. This method is used for DTA."""
        self.turning_prop.clear()

    def getTurningProp(self, i, j) -> float:
        """Returns the proportion of flow leaving Link i turning onto Link j. The value is between 0 and 1."""
        if len(self.getOutgoing()) <= 1:
            return 1
        if i in self.turning_prop and j in self.turning_prop[i]:
            return self.turning_prop[i][j]
        else:
            return 0.0

    def getIncoming(self) -> list:
        """Returns the list of incoming Links."""
        return self.incoming

    def getOutgoing(self) -> list:
        """Returns the list of outgoing Links."""
        return self.outgoing

    def addLink(self, link) -> None:
        """Adds the Link to the incoming or outgoing lists of links, as appropriate."""
        if link.getSource() is self:
            self.outgoing.append(link)
        elif link.getDest() is self:
            self.incoming.append(link)

    def getId(self) -> int:
        """Returns the id for this Node."""
        return self.id

    @abstractmethod
    def step(self) -> None:
        """Called every time step. For the Node class, step() should move flow between incoming and outgoing Links."""

    @abstractmethod
    def update(self) -> None:
        """Called every time step, after step() has been called for all Nodes and Links.

        It can be used to finish any updating work that could not occur during step().
        DO NOT use this to update the internal state of Links. This is used to update the state of this Node.
        """

    def __lt__(self, other: "Node") -> bool:
        """Used to sort Nodes by id."""
        return self.id < other.id

    def __hash__(self) -> int:
        """Used for hashing. You can ignore it."""
        return self.id

    def __repr__(self) -> str:
        """Returns the id of the Node."""
        return str(self.id)
