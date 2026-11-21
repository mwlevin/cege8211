"""Python version of ``dnl/Network.java``."""

from __future__ import annotations

import math
import traceback
import sys

from dnl.Params import Params
from dnl.Path import Path
from dnl.node.Sink import Sink
from dnl.node.Source import Source


class Network:
    """Represents and stores the entire network, including the lists of Nodes and Links.

    Generally, this will be the go-to class for dealing with the network as a whole.
    The easiest way to construct a new Network is to create an instance of ReadNetwork, then call
    ReadNetwork.createNetwork(name) with the name of the network folder.
    To calculate the state of the network at the next time step, call nextTimestep().
    There are also methods to get the lists of Nodes and Links, and the specific Node or Link with a given id.
    """

    def __init__(self, name: str, nodes: list, links: list):
        """Constructs the Network with the given Nodes and Links.

        In general, the easiest way to construct a Network will be to create a new ReadNetwork instance,
        then call ReadNetwork.createNetwork(name) with the name of the network folder.
        """
        self.nodes = nodes
        self.links = links
        self.name = name

    def getName(self) -> str:
        """Returns the name of the network."""
        return self.name

    def getNodes(self) -> list:
        """Returns the list of all Nodes."""
        return self.nodes

    def getLinks(self) -> list:
        """Returns the list of all Links."""
        return self.links

    def getNode(self, id: int):
        """Finds the Node with the given id. If none exists, returns None."""
        for n in self.nodes:
            if n.getId() == id:
                return n
        return None

    def getLink(self, *args):
        """Finds a Link. If none exists, returns None.

        getLink(id) returns the Link with the given id.
        getLink(i, j) returns the Link from Node i to Node j.
        """
        if len(args) == 1:
            id = args[0]
            for l in self.links:
                if l.getId() == id:
                    return l
            return None

        i, j = args
        for l in i.getOutgoing():
            if l.getDest() is j:
                return l
        return None

    def autograde(self, solutions) -> float:
        """Does the same work as simulate() but compares the exiting vehicles from each Sink node to the solution file.

        :param solutions: path to the solution.txt file
        :return: proportion of correct answers.
        """
        with open(solutions) as f:
            header = f.readline().split()
            rows = f.read().split()

        # header is "time", then the sink node ids, then "end"
        solOrder = []
        for token in header[1:]:
            try:
                solOrder.append(self.getNode(int(token)))
            except ValueError:
                break

        tokens = iter(rows)

        Params.time = 0

        count = 0
        correct = 0

        try:
            while Params.time <= Params.DURATION:
                self.nextTimestep()

                if int(next(tokens)) != Params.time - Params.dt:
                    raise RuntimeError("Time mismatch")

                for s in solOrder:
                    solution = float(next(tokens))
                    exiting = s.getNumExiting()

                    if solution > 0.1 or exiting > 0.1:
                        if abs(solution - exiting) <= 0.01:
                            correct += 1
                        count += 1
        except StopIteration:
            traceback.print_exc(file=sys.stderr)

        if count == 0:
            return math.nan
        return correct / count

    def printAutograde(self, output) -> None:
        """Simulates the network and writes the exiting vehicles from each Sink node to the given file.

        This is used to create the solution.txt files.
        """
        sinks = [n for n in self.nodes if isinstance(n, Sink)]

        with open(output, "w") as fileout:
            fileout.write("time")
            for n in sinks:
                fileout.write("\t" + str(n.getId()))
            fileout.write("\t end\n")

            Params.time = 0

            while Params.time <= Params.DURATION:
                self.nextTimestep()

                fileout.write(str(Params.time - Params.dt))

                for n in sinks:
                    fileout.write("\t" + repr(float(n.getNumExiting())))
                fileout.write("\n")

        # calculate the average travel time for each link
        for l in self.links:
            l.calculateTravelTime()

    def simulate(self) -> None:
        """Simulates traffic flow from the current time to Params.DURATION.

        It calls nextTimestep() for each time step.
        Calculates the link travel times using Link.calculateTravelTime().
        """
        while Params.time <= Params.DURATION:
            self.nextTimestep()

        # calculate the average travel time for each link
        for l in self.links:
            l.calculateTravelTime()

    def nextTimestep(self) -> None:
        """Calculates the state of the network at the next time step.

        First, it calls step() on all Links and Nodes.
        Then, it calls update() on all Links and Nodes.
        Nodes and Links should implement step() and update() according to their specific traffic flow behavior.
        """
        # calculate flow to move during the next time step
        for l in self.links:
            l.step()

        # calculate flow to move during the next time step
        for n in self.nodes:
            n.step()

        # actually move flow for the next time step
        for l in self.links:
            l.update()

        # actually move flow for the next time step
        for n in self.nodes:
            n.update()

        # Used to calculate average travel time.
        for l in self.links:
            l.logOccupancyTime()

        # update the current time
        Params.time += Params.dt

    def dijkstras(self, dest) -> None:
        """Runs all-to-one shortest path rooted at the specified destination node.

        This method sets the Node shortest path labels, Node.cost and Node.pred.
        """
        # fill this in
        pass

    def trace(self, origin, dest) -> Path:
        """After running dijkstras(dest), this method is used to find the shortest path between an origin and a destination."""
        curr = origin

        output = Path()

        while curr.pred is not None:
            output.append(curr.pred)
            curr = curr.pred.getDest()

        return output

    def shortestPath(self, origin, dest) -> Path:
        """Calls dijkstras(dest) then trace(origin, dest) to find the shortest path between two Nodes."""
        self.dijkstras(dest)
        return self.trace(origin, dest)

    def reset(self) -> None:
        """Resets the network to prepare for the next dynamic network loading.

        Calls Node.reset() and Link.reset() for all nodes and links.
        """
        Params.time = 0

        for n in self.nodes:
            n.reset()

        for l in self.links:
            l.reset()

    def msa(self, num_iterations: int) -> None:
        """Uses the method of successive averages to solve dynamic traffic assignment.

        Assumption: only one destination node (Sink node) exists in this network.

        :param num_iterations: the number of iterations
        """
        # delete turning proportions
        for n in self.nodes:
            n.clearTurningProportions()

        # find destination node
        dest = None
        for n in self.nodes:
            if isinstance(n, Sink):
                if dest is not None:
                    raise RuntimeError("DNL is not equipped to handle multiple destinations.")
                dest = n

        print("Iteration\tGap")

        for iteration in range(1, num_iterations + 1):
            lam = 1.0 / iteration

            self.assignFlow(lam, dest)

            self.simulate()
            self.reset()

            gap = self.calculateGap(dest)

            print(f"{iteration}\t{gap}")

    def assignFlow(self, lam: float, dest) -> None:
        """Finds the all-or-nothing assignment, and takes the convex combination with the current assignment.

        This is one step of the method of successive averages.
        Assumption: only one destination node (Sink node) exists in this network.

        :param lam: the step size (lambda)
        :param dest: the single destination Sink node in the network
        """
        # fill this in
        pass

    def calculateGap(self, dest) -> float:
        """Calculates the dynamic user equilibrium gap.

        Assumption: only one destination node (Sink node) exists in this network.

        :param dest: the single destination Sink node in the network
        :return: the dynamic user equilibrium gap
        """
        # fill this in
        return 0.0

    def getTSTT(self) -> float:
        """Returns the total system travel time (sec) from the last iteration."""
        output = 0.0

        for l in self.links:
            output += l.getTotalTT()

        return output
