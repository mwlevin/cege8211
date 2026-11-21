# CEGE 8211 dynamic network loading: Python version

This folder is a Python translation of the Java project in `../java`. The two versions have the same
classes, the same input files, and the same autograder, so you can do the homework in either language.

## Requirements

Python 3.8 or newer. No extra packages are needed.

## Running

Run commands from inside this `python` folder:

```
python Main.py                    # runs the PQ1 network, then grades HW1
python -m dnl.Autograde HW3.txt   # grades any homework file
```

The autograder prints your scores to the screen and writes all other program output to `log.txt`.
Each network's correct answers are in `networks/<name>/solution.txt`.

## Same names as Java

Every class, method, and field has the same name as in Java, and each class is in a file with the same
name. For example, `PointQueue.getSendingFlow()` is in `src/dnl/link/PointQueue.java` in Java and in
`dnl/link/PointQueue.py` in Python. Fields such as `turning_prop` or `cells` keep their Java names too
(use `self.cells` inside the class). The methods you need to write contain the comment `# fill this in`.

Python does not allow two methods with the same name, so `Network.getLink` accepts either form:
`getLink(id)` finds a link by id, and `getLink(i, j)` finds the link from node `i` to node `j`.
