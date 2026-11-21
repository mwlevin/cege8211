"""Python version of ``dnl/ReadNetwork.java``."""

from __future__ import annotations

import re

from dnl.Network import Network
from dnl.Params import Params, BASE_DIR

from dnl.link.CTM import CTM
from dnl.link.LTM import LTM
from dnl.link.MN import MN
from dnl.link.CentroidConnector import CentroidConnector
from dnl.link.PointQueue import PointQueue
from dnl.link.SpatialQueue import SpatialQueue

from dnl.node.Diverge import Diverge
from dnl.node.Merge import Merge
from dnl.node.PedSignal import PedSignal
from dnl.node.Series import Series
from dnl.node.Signal import Signal
from dnl.node.Sink import Sink
from dnl.node.Source import Source
from dnl.node.StopSign import StopSign


def _is_int(token: str) -> bool:
    try:
        int(token)
        return True
    except ValueError:
        return False


def _data_rows(path):
    """Yields (line, tokens) for each data row of an input file.

    Header lines are skipped until the first line that starts with an integer;
    reading stops at the first later line that does not start with an integer.
    """
    started = False
    with open(path) as f:
        for line in f:
            tokens = line.split()
            if not tokens:
                continue
            if _is_int(tokens[0]):
                started = True
                yield line, tokens
            elif started:
                return


class ReadNetwork:
    """Reads a network from the files in a networks/ folder."""

    # These are Node types. They are not case-sensitive.
    # They correspond to the type field in the nodes.txt input file.
    # They are used to identify the Node subclass that is to be constructed.
    SOURCE = "source"
    SINK = "sink"
    SERIES = "series"
    DIVERGE = "diverge"
    MERGE = "merge"
    SIGNAL = "signal"
    STOP_SIGN = "stop-sign"
    PED_SIGNAL = "ped-signal"

    # These are Link types. They are not case-sensitive.
    # They are used in the type field in the links.txt input file.
    CTM = "CTM"
    LTM = "LTM"
    CENTROID_CONNECTOR = "centroid-connector"
    POINT_QUEUE = "point-queue"
    SPATIAL_QUEUE = "spatial-queue"
    MN = "mn"

    def __init__(self):
        """Constructs a new ReadNetwork."""
        self.network_name = None
        self.nodesmap = None
        self.linksmap = None

    def createNetwork(self, name: str) -> Network:
        """Reads in the network with the given directory.

        For instance, if given the name "2-link", it will read in the network in the "networks/2-link" folder.
        """
        print("Creating network " + name)

        self.network_name = name

        self.nodesmap = {}
        self.linksmap = {}

        folder = BASE_DIR / "networks" / name

        self.readParams(folder / "params.txt")
        self.readNodes(folder / "nodes.txt")
        self.readLinks(folder / "links.txt")
        self.readSignals(folder / "signals.txt", folder / "phases.txt")

        self.readTurningProportions(folder / "turning_proportions.txt")
        self.readDemand(folder / "demand.txt")

        # sort nodes and links by id
        nodes = [self.nodesmap[i] for i in sorted(self.nodesmap)]
        links = [self.linksmap[i] for i in sorted(self.linksmap)]

        self.nodesmap = None
        self.linksmap = None

        return Network(name, nodes, links)

    def readParams(self, path) -> None:
        """Reads the global parameters (dt, duration, jam_density). The first line is a header."""
        try:
            with open(path) as f:
                f.readline()  # skip the header line
                tokens = f.read().split()
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self.network_name}/params.txt"')
            return

        for k in range(0, len(tokens) - 1, 2):
            key = tokens[k]
            value = float(tokens[k + 1])

            if key.lower() == "dt":
                Params.dt = int(value)
            elif key.lower() == "duration":
                Params.DURATION = int(value)
            elif key.lower() == "jam_density":
                Params.JAM_DENSITY = value

    def createNode(self, id: int, type: str, longitude: float, latitude: float, elevation: float):
        """Constructs a node with the given parameters. Elevation is in ft."""
        t = type.lower()
        if t == self.SOURCE.lower():
            return Source(id, longitude, latitude, elevation)
        elif t == self.SINK.lower():
            return Sink(id, longitude, latitude, elevation)
        elif t == self.SERIES.lower():
            return Series(id, longitude, latitude, elevation)
        elif t == self.DIVERGE.lower():
            return Diverge(id, longitude, latitude, elevation)
        elif t == self.MERGE.lower():
            return Merge(id, longitude, latitude, elevation)
        elif t == self.SIGNAL.lower():
            return Signal(id, longitude, latitude, elevation)
        elif t == self.STOP_SIGN.lower():
            return StopSign(id, longitude, latitude, elevation)
        elif t == self.PED_SIGNAL.lower():
            return PedSignal(id, longitude, latitude, elevation)
        else:
            raise RuntimeError("Node type not recognized: " + type)

    def createLink(self, id: int, type: str, source, dest, length: float, ffspeed: float,
                    capacity: float, numLanes: int):
        """Constructs a link with the given parameters.

        Capacity is in veh/hr. Free flow speed is in mi/hr. Length is in mi.
        """
        t = type.lower()
        if t == self.CTM.lower():
            return CTM(id, source, dest, length, ffspeed, capacity, numLanes)
        elif t == self.LTM.lower():
            return LTM(id, source, dest, length, ffspeed, capacity, numLanes)
        elif t == self.POINT_QUEUE.lower():
            return PointQueue(id, source, dest, length, ffspeed, capacity, numLanes)
        elif t == self.SPATIAL_QUEUE.lower():
            return SpatialQueue(id, source, dest, length, ffspeed, capacity, numLanes)
        elif t == self.CENTROID_CONNECTOR.lower():
            return CentroidConnector(id, source, dest, length, ffspeed, capacity, numLanes)
        elif t == self.MN.lower():
            return MN(id, source, dest, length, ffspeed, capacity, numLanes)
        else:
            raise RuntimeError("Link type not recognized: " + type)

    def readNodes(self, path) -> None:
        """Reads all nodes from the specified file. Header data is ignored."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            raise RuntimeError(f'Cannot find file "networks/{self.network_name}/nodes.txt"')

        for _, tok in rows:
            id = int(tok[0])
            type = tok[1]
            longitude = float(tok[2])
            latitude = float(tok[3])
            elevation = float(tok[4])

            node = self.createNode(id, type, longitude, latitude, elevation)

            self.nodesmap[node.getId()] = node

    def readLinks(self, path) -> None:
        """Reads all links from the specified file. Header data is ignored."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            raise RuntimeError(f'Cannot find file "networks/{self.network_name}/links.txt"')

        for _, tok in rows:
            id = int(tok[0])
            type = tok[1]
            source_id = int(tok[2])
            dest_id = int(tok[3])
            length = float(tok[4])
            ffspd = float(tok[5])
            capacityPerLane = float(tok[6])
            numLanes = int(tok[7])

            source = self.nodesmap.get(source_id)
            dest = self.nodesmap.get(dest_id)

            if source is None:
                raise RuntimeError(f"Source node not found: {source_id}")

            if dest is None:
                raise RuntimeError(f"Dest node not found: {dest_id}")

            link = self.createLink(id, type, source, dest, length, ffspd, capacityPerLane, numLanes)

            self.linksmap[link.getId()] = link

    def readDemand(self, path) -> None:
        """Reads the demand (incoming vehicles) from the given file."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            raise RuntimeError(f'Cannot find file "networks/{self.network_name}/demand.txt"')

        for _, tok in rows:
            node_id = int(tok[0])
            start_time = float(tok[1])
            end_time = float(tok[2])
            rate = float(tok[3])

            node = self.nodesmap.get(node_id)

            if node is None:
                raise RuntimeError(f"Cannot find node {node_id}")

            if not isinstance(node, Source):
                raise RuntimeError(f"Attempting to add demand to non-source node: {node_id}")

            node.addDemand(start_time, end_time, rate)

    def readTurningProportions(self, path) -> None:
        """Reads the turning proportions from the given file."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self.network_name}/turning_proportions.txt"')
            return

        for _, tok in rows:
            upstream_id = int(tok[0])
            downstream_id = int(tok[1])
            proportion = float(tok[2])

            upstream = self.linksmap.get(upstream_id)
            downstream = self.linksmap.get(downstream_id)

            if upstream is None and downstream is None:
                raise RuntimeError(f"Cannot find link pair: upstream: {upstream_id} downstream: {downstream_id}")

            if downstream is not None:
                downstream.getSource().storeTurningProportion(upstream, downstream, proportion)
            else:
                upstream.getDest().storeTurningProportion(upstream, downstream, proportion)

    def readSignals(self, signals, phases) -> None:
        """Reads the signal cycle data for all nodes.

        Note that signal cycle data will only be stored for nodes that are actual signals. Otherwise, it will be ignored.
        This method reads two files: first, it looks at signals.txt to read the offset.
        Then, it looks at phases.txt to read signal phases.
        """
        try:
            rows = list(_data_rows(signals))
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self.network_name}/signals.txt"')
            rows = []

        for _, tok in rows:
            node_id = int(tok[0])
            offset = float(tok[1])

            node = self.nodesmap.get(node_id)

            if node is None:
                raise RuntimeError(f"Cannot find node {node_id}")

            if isinstance(node, Signal):
                node.setOffset(offset)

        try:
            rows = list(_data_rows(phases))
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self.network_name}/phases.txt"')
            rows = []

        for line, _ in rows:
            # the first 7 columns are before the braces; the link ids are inside two pairs of braces
            tok = line.split("{")[0].split()
            node_id = int(tok[0])
            type = tok[1]
            sequence = int(tok[2])
            all_red = float(tok[3])
            yellow = float(tok[4])
            green = float(tok[5])
            num_moves = int(tok[6])

            braces = re.findall(r"\{([^}]*)\}", line)

            # ids of incoming links
            inc_links = braces[0].split(",")

            # ids of outgoing links
            out_links = braces[1].split(",")

            # this is a list of protected turning movements
            protected_turns = []

            for idx in range(num_moves):
                i_id = int(inc_links[idx].strip())
                j_id = int(out_links[idx].strip())

                i = self.linksmap.get(i_id)
                j = self.linksmap.get(j_id)

                if i is None:
                    raise RuntimeError(f"Cannot find link {i_id}")

                if j is None:
                    raise RuntimeError(f"Cannot find link {j_id}")

                protected_turns.append((i, j))

            node = self.nodesmap.get(node_id)

            if node is None:
                raise RuntimeError(f"Cannot find node {node_id}")

            if isinstance(node, Signal):
                node.addPhase(sequence, green, yellow, all_red, protected_turns)
