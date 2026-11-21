"""Entry point for running the project. Python version of ``dnl/Main.java``.

Run from the python/ folder with::

    python Main.py
"""

from dnl.Autograde import Autograde
from dnl.ReadNetwork import ReadNetwork


def main():
    read = ReadNetwork()
    network = read.createNetwork("PQ1")
    network.simulate()

    Autograde.gradeHW("HW1.txt")


if __name__ == "__main__":
    main()
