"""Python version of ``dnl/ReadNetwork.java``."""

from __future__ import annotations

import re

from dnl.network import Network
from dnl.params import Params, BASE_DIR

from dnl.link.ctm import CTM
from dnl.link.ltm import LTM
from dnl.link.mn import MN
from dnl.link.centroid_connector import CentroidConnector
from dnl.link.point_queue import PointQueue
from dnl.link.spatial_queue import SpatialQueue

from dnl.node.diverge import Diverge
from dnl.node.merge import Merge
from dnl.node.ped_signal import PedSignal
from dnl.node.series import Series
from dnl.node.signal import Signal
from dnl.node.sink import Sink
from dnl.node.source import Source
from dnl.node.stop_sign import StopSign


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
    CTM = "ctm"
    LTM = "ltm"
    CENTROID_CONNECTOR = "centroid-connector"
    POINT_QUEUE = "point-queue"
    SPATIAL_QUEUE = "spatial-queue"
    MN = "mn"

    def __init__(self):
        """Constructs a new ReadNetwork."""
        self._network_name = None
        self._nodesmap = None
        self._linksmap = None

    def create_network(self, name: str) -> Network:
        """Reads in the network with the given directory.

        For instance, if given the name "2-link", it will read in the network in the "networks/2-link" folder.
        """
        print("Creating network " + name)

        self._network_name = name

        self._nodesmap = {}
        self._linksmap = {}

        folder = BASE_DIR / "networks" / name

        self.read_params(folder / "params.txt")
        self.read_nodes(folder / "nodes.txt")
        self.read_links(folder / "links.txt")
        self.read_signals(folder / "signals.txt", folder / "phases.txt")

        self.read_turning_proportions(folder / "turning_proportions.txt")
        self.read_demand(folder / "demand.txt")

        # sort nodes and links by id
        nodes = [self._nodesmap[i] for i in sorted(self._nodesmap)]
        links = [self._linksmap[i] for i in sorted(self._linksmap)]

        self._nodesmap = None
        self._linksmap = None

        return Network(name, nodes, links)

    def read_params(self, path) -> None:
        """Reads the global parameters (dt, duration, jam_density). The first line is a header."""
        try:
            with open(path) as f:
                f.readline()  # skip the header line
                tokens = f.read().split()
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self._network_name}/params.txt"')
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

    def create_node(self, id: int, type: str, longitude: float, latitude: float, elevation: float):
        """Constructs a node with the given parameters. Elevation is in ft."""
        t = type.lower()
        if t == self.SOURCE:
            return Source(id, longitude, latitude, elevation)
        elif t == self.SINK:
            return Sink(id, longitude, latitude, elevation)
        elif t == self.SERIES:
            return Series(id, longitude, latitude, elevation)
        elif t == self.DIVERGE:
            return Diverge(id, longitude, latitude, elevation)
        elif t == self.MERGE:
            return Merge(id, longitude, latitude, elevation)
        elif t == self.SIGNAL:
            return Signal(id, longitude, latitude, elevation)
        elif t == self.STOP_SIGN:
            return StopSign(id, longitude, latitude, elevation)
        elif t == self.PED_SIGNAL:
            return PedSignal(id, longitude, latitude, elevation)
        else:
            raise RuntimeError("Node type not recognized: " + type)

    def create_link(self, id: int, type: str, source, dest, length: float, ffspeed: float,
                    capacity: float, num_lanes: int):
        """Constructs a link with the given parameters.

        Capacity is in veh/hr. Free flow speed is in mi/hr. Length is in mi.
        """
        t = type.lower()
        if t == self.CTM:
            return CTM(id, source, dest, length, ffspeed, capacity, num_lanes)
        elif t == self.LTM:
            return LTM(id, source, dest, length, ffspeed, capacity, num_lanes)
        elif t == self.POINT_QUEUE:
            return PointQueue(id, source, dest, length, ffspeed, capacity, num_lanes)
        elif t == self.SPATIAL_QUEUE:
            return SpatialQueue(id, source, dest, length, ffspeed, capacity, num_lanes)
        elif t == self.CENTROID_CONNECTOR:
            return CentroidConnector(id, source, dest, length, ffspeed, capacity, num_lanes)
        elif t == self.MN:
            return MN(id, source, dest, length, ffspeed, capacity, num_lanes)
        else:
            raise RuntimeError("Link type not recognized: " + type)

    def read_nodes(self, path) -> None:
        """Reads all nodes from the specified file. Header data is ignored."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            raise RuntimeError(f'Cannot find file "networks/{self._network_name}/nodes.txt"')

        for _, tok in rows:
            id = int(tok[0])
            type = tok[1]
            longitude = float(tok[2])
            latitude = float(tok[3])
            elevation = float(tok[4])

            node = self.create_node(id, type, longitude, latitude, elevation)

            self._nodesmap[node.get_id()] = node

    def read_links(self, path) -> None:
        """Reads all links from the specified file. Header data is ignored."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            raise RuntimeError(f'Cannot find file "networks/{self._network_name}/links.txt"')

        for _, tok in rows:
            id = int(tok[0])
            type = tok[1]
            source_id = int(tok[2])
            dest_id = int(tok[3])
            length = float(tok[4])
            ffspd = float(tok[5])
            capacity_per_lane = float(tok[6])
            num_lanes = int(tok[7])

            source = self._nodesmap.get(source_id)
            dest = self._nodesmap.get(dest_id)

            if source is None:
                raise RuntimeError(f"Source node not found: {source_id}")

            if dest is None:
                raise RuntimeError(f"Dest node not found: {dest_id}")

            link = self.create_link(id, type, source, dest, length, ffspd, capacity_per_lane, num_lanes)

            self._linksmap[link.get_id()] = link

    def read_demand(self, path) -> None:
        """Reads the demand (incoming vehicles) from the given file."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            raise RuntimeError(f'Cannot find file "networks/{self._network_name}/demand.txt"')

        for _, tok in rows:
            node_id = int(tok[0])
            start_time = float(tok[1])
            end_time = float(tok[2])
            rate = float(tok[3])

            node = self._nodesmap.get(node_id)

            if node is None:
                raise RuntimeError(f"Cannot find node {node_id}")

            if not isinstance(node, Source):
                raise RuntimeError(f"Attempting to add demand to non-source node: {node_id}")

            node.add_demand(start_time, end_time, rate)

    def read_turning_proportions(self, path) -> None:
        """Reads the turning proportions from the given file."""
        try:
            rows = list(_data_rows(path))
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self._network_name}/turning_proportions.txt"')
            return

        for _, tok in rows:
            upstream_id = int(tok[0])
            downstream_id = int(tok[1])
            proportion = float(tok[2])

            upstream = self._linksmap.get(upstream_id)
            downstream = self._linksmap.get(downstream_id)

            if upstream is None and downstream is None:
                raise RuntimeError(f"Cannot find link pair: upstream: {upstream_id} downstream: {downstream_id}")

            if downstream is not None:
                downstream.get_source().store_turning_proportion(upstream, downstream, proportion)
            else:
                upstream.get_dest().store_turning_proportion(upstream, downstream, proportion)

    def read_signals(self, signals, phases) -> None:
        """Reads the signal cycle data for all nodes.

        Note that signal cycle data will only be stored for nodes that are actual signals. Otherwise, it will be ignored.
        This method reads two files: first, it looks at signals.txt to read the offset.
        Then, it looks at phases.txt to read signal phases.
        """
        try:
            rows = list(_data_rows(signals))
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self._network_name}/signals.txt"')
            rows = []

        for _, tok in rows:
            node_id = int(tok[0])
            offset = float(tok[1])

            node = self._nodesmap.get(node_id)

            if node is None:
                raise RuntimeError(f"Cannot find node {node_id}")

            if isinstance(node, Signal):
                node.set_offset(offset)

        try:
            rows = list(_data_rows(phases))
        except FileNotFoundError:
            print(f'\tSkipping file "networks/{self._network_name}/phases.txt"')
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

                i = self._linksmap.get(i_id)
                j = self._linksmap.get(j_id)

                if i is None:
                    raise RuntimeError(f"Cannot find link {i_id}")

                if j is None:
                    raise RuntimeError(f"Cannot find link {j_id}")

                protected_turns.append((i, j))

            node = self._nodesmap.get(node_id)

            if node is None:
                raise RuntimeError(f"Cannot find node {node_id}")

            if isinstance(node, Signal):
                node.add_phase(sequence, green, yellow, all_red, protected_turns)
