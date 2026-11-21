# CEGE 8211 dynamic network loading: Python version

This folder is a Python translation of the Java project in `../java`. The two versions have the same
classes, the same input files, and the same autograder, so you can do the homework in either language.

## Requirements

Python 3.8 or newer. No extra packages are needed.

## Running

Run commands from inside this `python` folder:

```
python main.py                    # runs the PQ1 network, then grades HW1
python -m dnl.autograde HW3.txt   # grades any homework file
```

The autograder prints your scores to the screen and writes all other program output to `log.txt`.
Each network's correct answers are in `networks/<name>/solution.txt`.

## Where things are

| Java (`../java/src/dnl/...`) | Python (`dnl/...`)          |
|------------------------------|-----------------------------|
| `Main.java`                  | `../main.py`                |
| `Params.java`                | `params.py`                 |
| `Network.java`               | `network.py`                |
| `ReadNetwork.java`           | `read_network.py`           |
| `Autograde.java`             | `autograde.py`              |
| `Path.java`                  | `path.py`                   |
| `link/PointQueue.java`       | `link/point_queue.py`       |
| `link/SpatialQueue.java`     | `link/spatial_queue.py`     |
| `link/CTM.java`, `Cell.java` | `link/ctm.py`, `link/cell.py` |
| `link/LTM.java`              | `link/ltm.py`               |
| `node/Merge.java`, ...       | `node/merge.py`, ...        |

Method names use Python style: Java's `getSendingFlow()` is `get_sending_flow()`, `addFlow(y)` is
`add_flow(y)`, and so on. The methods you need to write contain the comment `# fill this in`.

## Differences from Java worth knowing

- **Global parameters** are class attributes: use `Params.dt`, `Params.time`, `Params.DURATION`, and
  `Params.JAM_DENSITY` (import with `from dnl.params import Params`).
- **Rounding:** Python's `round()` rounds halves to the nearest even number (`round(2.5) == 2`), but
  Java's `Math.round()` rounds halves up. To match the solutions, use `int(math.floor(x + 0.5))`.
- **Division by zero** raises an error in Python instead of giving `Infinity` or `NaN`.
- **Queues:** `collections.deque` works like Java's `LinkedList`: `append()` adds to the end,
  `popleft()` removes from the front, `q[0]` is the first item, and `q[-1]` is the last.
- **Infinity:** `INTEGER_MAX_VALUE` and `DOUBLE_MAX_VALUE` in `params.py` match Java's
  `Integer.MAX_VALUE` and `Double.MAX_VALUE`. `math.inf` also works.
- `Network.get_link(id)` finds a link by id. Java's `getLink(Node i, Node j)` is
  `get_link_between(i, j)` in Python.
