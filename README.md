Maze Solver

A Python-based maze generation and solving system with real-time visualization using Pygame.

Overview

This project implements multiple algorithms for both generating and solving mazes. It includes support for creating extremely large mazes with up to 50 million cells and provides interactive visualization during generation and solving.

Features

Maze Generation: Creates perfect mazes using recursive backtracking algorithm
Large Maze Support: Can generate mazes with up to 50 million cells
Real-time Visualization: Watch mazes being generated and solved in real-time
Multiple Solving Algorithms: Recursive backtracking and dead end filling methods
Multiple Size Presets: Choose from small, medium, large, or custom maze sizes
Efficient Storage: Automatically saves mazes in JSON format with numpy array support for large mazes
Interactive Solving: Visual maze solving with step counting and time tracking
Image Export: Export mazes as PNG images for manual solving
Optimized Performance: Designed for Mac M1 Air 8GB with lag prevention

Files

maze.py: Basic maze generator for small to medium sized mazes
large_maze_generator.py: Advanced generator for creating massive mazes (up to 50M cells)
recursive_backtracking.py: Maze solver using recursive backtracking with visualization
dead_end_solver.py: Maze solver using dead end filling algorithm with visualization
export_maze_image.py: Utility to export existing mazes as PNG images for manual solving

Requirements

Python 3.x
NumPy
Pygame

Installation

Install the required dependencies:

pip install numpy pygame

Usage

Generating a Standard Maze

python maze.py

This will create a maze and save it to the mazes directory.

Generating a Large Maze

python large_maze_generator.py

Follow the interactive prompts to select maze size and visualization options.

Solving a Maze

Option 1: Recursive Backtracking

python recursive_backtracking.py

This will automatically load and solve the most recently generated maze using recursive backtracking.

Option 2: Dead End Filling

python dead_end_solver.py

This will solve the maze by iteratively filling in all dead ends until only the solution path remains.

Exporting Maze as Image

python export_maze_image.py

This will convert any maze to a PNG image that you can print and solve by hand.

How It Works

Maze Generation

The generator uses recursive backtracking to carve passages through a grid of walls. Starting from a random cell, it randomly chooses unvisited neighboring cells and creates paths between them. When it reaches a dead end, it backtracks to find unexplored paths.

Maze Solving Algorithms

Recursive Backtracking

The solver explores all possible paths from the start position. It marks cells as visited and backtracks when it hits a dead end. This continues until the end position is found. The algorithm guarantees finding a solution if one exists.

Dead End Filling

This algorithm identifies and fills in all dead ends (passages with only one open neighbor) iteratively. It continues filling dead ends until no more exist. What remains is the solution path from start to end. This method is often faster for complex mazes and provides a clear visualization of the solution process.

Technical Details

Mazes are stored as numpy arrays where 1 represents walls and 0 represents passages
Start position is always at (1, 1)
End position is always at (height-2, width-2)
All maze dimensions are odd numbers to ensure proper wall and passage structure
Large mazes are saved as separate .npy files for efficient storage and loading

Performance

Optimized for Mac M1 Air 8GB with lag prevention
Can handle mazes up to 50 million cells
Adaptive visualization updates based on maze size
Automatic visualization disabling for very large mazes to prevent lag
Cell sizes automatically adjusted for clear visibility without zooming
Progress tracking provides feedback during long generation times

Output

Generated mazes are saved in the mazes/ directory with timestamps
Each maze file includes metadata such as dimensions, start/end positions, and generation timestamp
Solved mazes are updated with solution paths, step counts, and solve times

Author

Created by Saagnik Mondal

License

This project is open source and available for educational and personal use.
