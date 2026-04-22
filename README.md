*This project has been created as part of the 42 curriculum by \<login1\>[, \<login2\>[, \<login3\>]].*

# A-Maze-ing 🌀

## Description

A-Maze-ing is a Python maze generator that creates random mazes from a configuration file and outputs them in a hexadecimal wall-encoding format. The program supports both perfect mazes (exactly one path between entry and exit) and imperfect mazes, includes a visual "42" pattern embedded in the maze, and provides an interactive terminal or graphical display with pathfinding.

Key features:
- Random maze generation with optional seed for reproducibility
- Perfect maze support (unique path from entry to exit)
- Hexadecimal output file format encoding wall states per cell
- Visual representation via terminal (ASCII/color) or MiniLibX (MLX)
- Interactive controls: regenerate, show/hide solution path, change wall colors
- Embedded "42" pattern made of fully closed cells
- Reusable `MazeGenerator` class packaged as a pip-installable module (`mazegen-*`)

---

## Instructions

### Requirements

- Python 3.10 or later
- `pip`, `uv`, or `pipx` for dependency management
- (Optional) MiniLibX for graphical display

### Installation

```bash
make install
```

### Running

```bash
make run
# or directly:
python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug
```

### Linting

```bash
make lint
# optional strict mode:
make lint-strict
```

### Cleaning

```bash
make clean
```

---

## Configuration File

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

### Mandatory Keys

| Key           | Description                        | Example                  |
|---------------|------------------------------------|--------------------------|
| `WIDTH`       | Maze width in cells                | `WIDTH=20`               |
| `HEIGHT`      | Maze height in cells               | `HEIGHT=15`              |
| `ENTRY`       | Entry coordinates (x,y)            | `ENTRY=0,0`              |
| `EXIT`        | Exit coordinates (x,y)             | `EXIT=19,14`             |
| `OUTPUT_FILE` | Output filename                    | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`     | Whether the maze is perfect        | `PERFECT=True`           |

### Optional Keys

| Key         | Description                                      | Example              |
|-------------|--------------------------------------------------|----------------------|
| `SEED`      | Integer seed for reproducible generation         | `SEED=42`            |
| `ALGORITHM` | Generation algorithm (`recursive`, `prim`, etc.) | `ALGORITHM=recursive`|
| `DISPLAY`   | Display mode (`terminal` or `mlx`)               | `DISPLAY=terminal`   |

### Example `config.txt`

```
# A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=recursive
DISPLAY=terminal
```

---

## Output File Format

Each cell is encoded as a single hexadecimal digit where each bit indicates a closed wall:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

- Bit = `1` → wall is **closed**
- Bit = `0` → wall is **open**

Cells are written row by row, one row per line. After the grid, an empty line is followed by three lines:
1. Entry coordinates (`x,y`)
2. Exit coordinates (`x,y`)
3. Shortest path from entry to exit using `N`, `E`, `S`, `W`

**Example:**
```
9515391539551795151151153
EBABAE812853C1412BA812812
...

1,1
19,14
SWSESWSESWSSSEESEEENEESESEESSSSEEESSSEEENNENEE
```

---

## Maze Generation Algorithm

This project uses the **Recursive Backtracker** (depth-first search) algorithm.

### Why this algorithm?

- Produces long, winding corridors that make for challenging and visually interesting mazes
- Naturally generates **perfect mazes** (a single unique path between any two cells), which is a core requirement of this project
- Simple to implement and easy to extend with a seed for reproducibility
- Straightforward to constrain for the "no 3×3 open area" rule and the embedded "42" pattern

---

## Visual Representation

The program offers two display modes:

**Terminal (default):** Renders the maze using colored ASCII characters in the terminal.

**MiniLibX (MLX):** Opens a graphical window for a richer visual experience.

### Interactive Controls

| Action | Terminal | MLX |
|--------|----------|-----|
| Re-generate maze | `1` | `1` |
| Show/Hide solution path | `2` | `2` |
| Rotate/Change wall colors | `3` | `3` |
| Quit | `4` | `4` |

---

## Reusable Module — `mazegen`

The maze generation logic is packaged as a standalone pip-installable module.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or
pip install mazegen-1.0.0.tar.gz
```

### Basic Usage

```python
from mazegen import MazeGenerator

# Instantiate with width, height, and optional seed
gen = MazeGenerator(width=20, height=15, seed=42)

# Generate a perfect maze
gen.generate(perfect=True)

# Access the maze grid (2D list of wall bitmasks)
grid = gen.maze  # grid[row][col] is an int 0–15

# Get the shortest solution path
solution = gen.solve(entry=(0, 0), exit=(19, 14))
# Returns a list of directions: ['S', 'E', 'E', ...]

# Access entry/exit
print(gen.entry)  # (0, 0)
print(gen.exit)   # (19, 14)
```

### Custom Parameters

```python
gen = MazeGenerator(
    width=30,
    height=20,
    seed=123,
    algorithm="prim"  # if multiple algorithms are supported
)
gen.generate(perfect=False)
```

> **Note:** The internal `maze` grid uses the same bitmask encoding as the output file (bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West), but the module exposes it as a Python list of lists — not the flat text file format.

### Building the Package

```bash
python3 -m pip install build
python3 -m build
# Output: dist/mazegen-1.0.0-py3-none-any.whl and dist/mazegen-1.0.0.tar.gz
```

---

## Team & Project Management

### Roles

| Member | Role |
|--------|------|
| `<login1>` | Maze generation algorithm, core logic, reusable module |
| `<login2>` | Output file format, config parser, error handling |
| `<login3>` | Visual display (terminal + MLX), pathfinding, UI interactions |

### Planning

**Week 1:** Project setup, config parser, core maze data structures, algorithm research  
**Week 2:** Recursive backtracker implementation, output file generation, "42" pattern embedding  
**Week 3:** Visual display (terminal ASCII), BFS pathfinding, interactive controls  
**Week 4:** MLX graphical display, reusable package setup, README, linting, testing  

The initial plan was optimistic on the MLX display timeline — it took longer than expected to handle window events cleanly. The "42" pattern placement also required more iteration to ensure it didn't break maze connectivity.

### What Worked Well

- The recursive backtracker naturally produces clean perfect mazes
- Splitting generation and display into separate modules made testing much easier
- Using a seed from the start made debugging consistent

### What Could Be Improved

- The 3×3 open area constraint adds complexity to post-processing; integrating it directly into generation would be cleaner
- MLX event handling could be abstracted further for easier extension

### Tools Used

- **Python 3.11** — main language
- **flake8 + mypy** — linting and type checking
- **pytest** — unit testing
- **build / pip** — package management
- **MiniLibX** — graphical display
- **Claude (Anthropic)** — used to help draft docstrings, brainstorm algorithm tradeoffs, and review the README structure. All generated content was reviewed, tested, and rewritten as needed by the team.

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker — Think Labyrinth](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Spanning trees and perfect mazes](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Python `typing` module — docs](https://docs.python.org/3/library/typing.html)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

### AI Usage

Claude (claude.ai) was used to assist with:
- Drafting and structuring this README
- Reviewing docstring style for PEP 257 compliance
- Discussing tradeoffs between maze generation algorithms (recursive backtracker vs. Prim's vs. Kruskal's)

All AI-generated suggestions were critically reviewed, tested, and adapted by the team. No AI-generated code was used without full understanding and manual validation.
