"""Entry point for running the project. Python version of ``dnl/Main.java``.

Run from the python/ folder with::

    python main.py
"""

from dnl import autograde
from dnl.read_network import ReadNetwork


def main():
    read = ReadNetwork()
    network = read.create_network("PQ1")
    network.simulate()

    autograde.grade_hw("HW1.txt")


if __name__ == "__main__":
    main()
