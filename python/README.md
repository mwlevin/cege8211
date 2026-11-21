# CEGE 8211 dynamic network loading: Python

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

## Code

Each class is in a file with the same name, e.g. `PointQueue` is in `dnl/link/PointQueue.py`.
The methods you need to write contain the comment `# fill this in`.
