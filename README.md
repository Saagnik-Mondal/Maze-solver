# Maze Generator & Solver (Python, Pygame, NumPy)

A Python-based project to generate, visualize, and solve mazes in real time using multiple algorithms. Built to experiment with maze logic, performance optimization, and algorithmic problem-solving — scalable from small grids to tens of millions of cells.

## Features
Real-time maze generation and solving visualization using Pygame
Supports very large mazes (tested up to 50 million cells)
Multiple maze-solving algorithms implemented and compared
Automatic performance optimizations for large-scale mazes
Export mazes as PNG images for offline or manual solving
Automatic saving and loading of generated mazes

## Maze Generation
Uses recursive backtracking (depth-first search) to carve paths
Starts from a random cell and explores neighbors
Backtracks when no unvisited paths remain
Guarantees a fully connected maze with a single solution

## Maze Solving Algorithms
Recursive Backtracking
Explores all possible paths until the exit is found
Dead-End Filling
Iteratively removes dead ends until only the correct path remains
Left-Hand Rule
Wall-following approach that simulates real-world maze navigation

## Technical Details
Mazes stored as NumPy arrays (1 = wall, 0 = path)
Start position: (1, 1)
Exit position: (height-2, width-2)
Large mazes saved as .npy files to reduce memory usage
Visualization automatically disables for extremely large mazes
Cell sizes adjust dynamically based on maze dimensions
All outputs saved with timestamps in the mazes/ directory

## The Files

- `maze.py` - basic maze generator, good for quick testing
- `large_maze_generator.py` - for when you want to go crazy with size
- `recursive_backtracking.py` - classic depth-first maze solver
- `dead_end_solver.py` - fills in dead ends until only the solution remains
- `left_hand_algo.py` - wall-following solver (like you'd do with your hand on the wall)
- `export_maze_image.py` - converts mazes to PNG images

## Getting Started

You'll need Python 3 and a couple packages:

```bash
pip install numpy pygame
```

## How to Use

**Make a basic maze:**
```bash
python maze.py
```

**Make a big maze:**
```bash
python large_maze_generator.py
```
Just follow the prompts to pick the size.

**Solve a maze:**
```bash
python recursive_backtracking.py
# or
python dead_end_solver.py
# or
python left_hand_algo.py
```

**Export as image:**
```bash
python export_maze_image.py
```

## How It Actually Works

### Generation
Starts at a random spot and carves paths by visiting neighbors. When it hits a wall, it backtracks and tries a different route. Keeps going until the whole maze is carved out.

### Solving
- **Recursive backtracking** - tries every possible path until it finds the exit
- **Dead end filling** - keeps filling in dead ends until only the solution path is left
- **Left-hand rule** - follows the left wall until you reach the exit (like you'd do in a real maze)

## Some Details

- Mazes are stored as numpy arrays (1 = wall, 0 = path)
- Start is always top-left corner at (1, 1)
- Exit is always bottom-right at (height-2, width-2)
- Big mazes get saved as .npy files to save space
- Everything gets saved in the `mazes/` folder with timestamps

## Performance Notes

I optimized this for my M1 Air with 8GB RAM. It handles up to 50M cells pretty well. For really huge mazes, the visualization auto-disables to prevent lag. Cell sizes adjust automatically so you don't need to zoom in.

## Author
## Saagnik Mondal
