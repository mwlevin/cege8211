"""Autograder: compares simulation results to the answers in networks/<name>/solution.txt.

Run from the python/ folder with, e.g.::

    python -m dnl.Autograde HW1.txt
"""

from __future__ import annotations

import math
import sys
from pathlib import Path as FilePath

from dnl.Params import BASE_DIR
from dnl.ReadNetwork import ReadNetwork


def _resolve(path) -> FilePath:
    """Interprets relative paths relative to the python/ folder unless they exist in the current directory."""
    p = FilePath(path)
    if p.is_absolute() or p.exists():
        return p
    return BASE_DIR / p


def _percent(x: float) -> int:
    """Rounds a proportion to a whole percent (halves round up)."""
    if math.isnan(x):
        return 0
    return int(math.floor(x * 100.0 + 0.5))


def _readTestCases(testCases):
    """Reads a HW file. Yields (name, description, num_iter); num_iter is None unless DTA is enabled.

    Each line contains the name of a test case, e.g. PQ1 corresponds to the "networks/PQ1/" network,
    optionally followed by a description. A line "DTA <n>" means that the following test cases first
    run <n> iterations of the method of successive averages.
    """
    num_iter = None
    with open(_resolve(testCases)) as f:
        for line in f:
            tokens = line.split()
            if not tokens:
                continue
            if tokens[0].lower() == "dta":
                num_iter = int(tokens[1])
                continue
            name = tokens[0]
            description = line.strip()[len(name):].strip()
            if len(description) == 0:
                description = name
            yield name, description, num_iter


class Autograde:

    @staticmethod
    def gradeHW(testCases) -> float:
        """Grades the test cases listed in the given file.

        Each line of the file contains the name of a test case, e.g. PQ1 corresponds to the "networks/PQ1/" network.
        Returns a number between 0 and 1 indicating the proportion correct. Each test case is weighted equally.
        Normal program output is written to log.txt; the scores are printed to the screen.
        """
        total = 0
        correct = 0.0

        old_stdout = sys.stdout
        with open(BASE_DIR / "log.txt", "w") as log:
            sys.stdout = log
            try:
                print(f"Grading {testCases} tests\n", file=sys.stderr)
                print("-------", file=sys.stderr)

                for name, description, num_iter in _readTestCases(testCases):
                    if num_iter is not None:
                        output = Autograde.gradeNetworkDTA(name, num_iter)
                    else:
                        output = Autograde.gradeNetwork(name)

                    print(f"Running {description} test: networks/{name}/", file=sys.stderr)
                    print(f"\tScore: {_percent(output)}%", file=sys.stderr)
                    correct += output

                    total += 1
            finally:
                sys.stdout = old_stdout

        print("-------", file=sys.stderr)
        print(f"Total: {_percent(correct / total)}%", file=sys.stderr)
        print("\nThis is an unofficial score, please submit code for final scoring.", file=sys.stderr)
        return correct / total

    @staticmethod
    def gradeNetwork(name: str) -> float:
        read = ReadNetwork()
        network = read.createNetwork(name)

        return network.autograde(BASE_DIR / "networks" / name / "solution.txt")

    @staticmethod
    def gradeNetworkDTA(name: str, num_iter: int) -> float:
        read = ReadNetwork()
        network = read.createNetwork(name)

        network.msa(num_iter)

        return network.autograde(BASE_DIR / "networks" / name / "solution.txt")

    @staticmethod
    def createSolutions(testCases) -> None:
        """Writes networks/<name>/solution.txt for every test case in the given file (instructor use)."""
        for name, _, num_iter in _readTestCases(testCases):
            read = ReadNetwork()
            network = read.createNetwork(name)

            if num_iter is not None:
                network.msa(num_iter)

            network.printAutograde(BASE_DIR / "networks" / name / "solution.txt")


if __name__ == "__main__":
    Autograde.gradeHW(sys.argv[1] if len(sys.argv) > 1 else "HW2.txt")
