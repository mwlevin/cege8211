"""Python version of ``dnl/Network.java``."""

from __future__ import annotations

import math
import traceback
import sys

from dnl.params import Params
from dnl.path import Path
from dnl.node.sink import Sink
from dnl.node.source import Source


class Network:
    """Represents and stores the entire network, including the lists of Nodes and Links.

    Generally, this will be the go-to class for dealing with the network as a whole.
    The easiest way to construct a new Network is to create an instance of ReadNetwork, then call
    ReadNetwork.create_network(name) with the name of the network folder.
    To calculate the state of the network at the next time step, call next_timestep().
    There are also methods to get the lists of Nodes and Links, and the specific Node or Link with a given id.
    """

    def __init__(self, name: str, nodes: list, links: list):
        """Constructs the Network with the given Nodes and Links.

        In general, the easiest way to construct a Network will be to create a new ReadNetwork instance,
        then call ReadNetwork.create_network(name) with the name of the network folder.
        """
        self._nodes = nodes
        self._links = links
        self._name = name

    def get_name(self) -> str:
        """Returns the name of the network."""
        return self._name

    def get_nodes(self) -> list:
        """Returns the list of all Nodes."""
        return self._nodes

    def get_links(self) -> list:
        """Returns the list of all Links."""
        return self._links

    def get_node(self, id: int):
        """Finds the Node with the given id. If none exists, returns None."""
        for n in self._nodes:
            if n.get_id() == id:
                return n
        return None

    def get_link(self, id: int):
        """Finds the Link with the given id. If none exists, returns None."""
        for l in self._links:
            if l.get_id() == id:
                return l
        return None

    def get_link_between(self, i, j):
        """Returns the Link from Node i to Node j, or None if none exists."""
        for l in i.get_outgoing():
            if l.get_dest() is j:
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
        sol_order = []
        for token in header[1:]:
            try:
                sol_order.append(self.get_node(int(token)))
            except ValueError:
                break

        tokens = iter(rows)

        Params.time = 0

        count = 0
        correct = 0

        try:
            while Params.time <= Params.DURATION:
                self.next_timestep()

                if int(next(tokens)) != Params.time - Params.dt:
                    raise RuntimeError("Time mismatch")

                for s in sol_order:
                    solution = float(next(tokens))
                    exiting = s.get_num_exiting()

                    if solution > 0.1 or exiting > 0.1:
                        if abs(solution - exiting) <= 0.01:
                            correct += 1
                        count += 1
        except StopIteration:
            traceback.print_exc(file=sys.stderr)

        if count == 0:
            return math.nan
        return correct / count

    def print_autograde(self, output) -> None:
        """Simulates the network and writes the exiting vehicles from each Sink node to the given file.

        This is used to create the solution.txt files.
        """
        sinks = [n for n in self._nodes if isinstance(n, Sink)]

        with open(output, "w") as fileout:
            fileout.write("time")
            for n in sinks:
                fileout.write("\t" + str(n.get_id()))
            fileout.write("\t end\n")

            Params.time = 0

            while Params.time <= Params.DURATION:
                self.next_timestep()

                fileout.write(str(Params.time - Params.dt))

                for n in sinks:
                    fileout.write("\t" + repr(float(n.get_num_exiting())))
                fileout.write("\n")

        # calculate the average travel time for each link
        for l in self._links:
            l.calculate_travel_time()

    def simulate(self) -> None:
        """Simulates traffic flow from the current time to Params.DURATION.

        It calls next_timestep() for each time step.
        Calculates the link travel times using Link.calculate_travel_time().
        """
        while Params.time <= Params.DURATION:
            self.next_timestep()

        # calculate the average travel time for each link
        for l in self._links:
            l.calculate_travel_time()

    def next_timestep(self) -> None:
        """Calculates the state of the network at the next time step.

        First, it calls step() on all Links and Nodes.
        Then, it calls update() on all Links and Nodes.
        Nodes and Links should implement step() and update() according to their specific traffic flow behavior.
        """
        # calculate flow to move during the next time step
        for l in self._links:
            l.step()

        # calculate flow to move during the next time step
        for n in self._nodes:
            n.step()

        # actually move flow for the next time step
        for l in self._links:
            l.update()

        # actually move flow for the next time step
        for n in self._nodes:
            n.update()

        # Used to calculate average travel time.
        for l in self._links:
            l.log_occupancy_time()

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
            curr = curr.pred.get_dest()

        return output

    def shortest_path(self, origin, dest) -> Path:
        """Calls dijkstras(dest) then trace(origin, dest) to find the shortest path between two Nodes."""
        self.dijkstras(dest)
        return self.trace(origin, dest)

    def reset(self) -> None:
        """Resets the network to prepare for the next dynamic network loading.

        Calls Node.reset() and Link.reset() for all nodes and links.
        """
        Params.time = 0

        for n in self._nodes:
            n.reset()

        for l in self._links:
            l.reset()

    def msa(self, num_iterations: int) -> None:
        """Uses the method of successive averages to solve dynamic traffic assignment.

        Assumption: only one destination node (Sink node) exists in this network.

        :param num_iterations: the number of iterations
        """
        # delete turning proportions
        for n in self._nodes:
            n.clear_turning_proportions()

        # find destination node
        dest = None
        for n in self._nodes:
            if isinstance(n, Sink):
                if dest is not None:
                    raise RuntimeError("DNL is not equipped to handle multiple destinations.")
                dest = n

        print("Iteration\tGap")

        for iteration in range(1, num_iterations + 1):
            lam = 1.0 / iteration

            self.assign_flow(lam, dest)

            self.simulate()
            self.reset()

            gap = self.calculate_gap(dest)

            print(f"{iteration}\t{gap}")

    def assign_flow(self, lam: float, dest) -> None:
        """Finds the all-or-nothing assignment, and takes the convex combination with the current assignment.

        This is one step of the method of successive averages.
        Assumption: only one destination node (Sink node) exists in this network.

        :param lam: the step size (lambda)
        :param dest: the single destination Sink node in the network
        """
        # fill this in
        pass

    def calculate_gap(self, dest) -> float:
        """Calculates the dynamic user equilibrium gap.

        Assumption: only one destination node (Sink node) exists in this network.

        :param dest: the single destination Sink node in the network
        :return: the dynamic user equilibrium gap
        """
        # fill this in
        return 0.0

    def get_tstt(self) -> float:
        """Returns the total system travel time (sec) from the last iteration."""
        output = 0.0

        for l in self._links:
            output += l.get_total_tt()

        return output
