# Maze Solver

Generate and solve mazes with Python. Watch them get built and solved in real-time.

## What's This?

I built this to play around with maze algorithms. You can generate mazes (including ridiculously large ones with 50 million cells if you're feeling adventurous) and solve them using different methods. Everything runs with Pygame for visualization.

## What Can It Do?

- Generate mazes using recursive backtracking
- Make huge mazes - tested up to 50M cells on my M1 Air
- Watch mazes being created and solved in real-time
- Three different solving methods (recursive backtracking, dead end filling, left-hand rule)
- Export mazes as PNG if you want to solve them on paper
- Saves everything automatically so you can come back to it later

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

---

Made by Saagnik Mondal

Feel free to use this for whatever you want.
