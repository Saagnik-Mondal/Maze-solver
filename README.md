Maze Solver

A Python-based maze generation and solving system with real-time visualization using Pygame.

Overview

This project implements recursive backtracking algorithms for both generating and solving mazes. It includes support for creating extremely large mazes with over 30 million cells and provides interactive visualization during generation and solving.

Features

Maze Generation: Creates perfect mazes using recursive backtracking algorithm
Large Maze Support: Can generate mazes with 30+ million cells (up to 100M cells)
Real-time Visualization: Watch mazes being generated and solved in real-time
Multiple Size Presets: Choose from small, medium, large, or custom maze sizes
Efficient Storage: Automatically saves mazes in JSON format with numpy array support for large mazes
Interactive Solving: Visual maze solving with step counting and time tracking

Files

maze.py: Basic maze generator for small to medium sized mazes
large_maze_generator.py: Advanced generator for creating massive mazes (30M+ cells)
recursive_backtracking.py: Maze solver with Pygame visualization

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

python recursive_backtracking.py

This will automatically load and solve the most recently generated maze with visual feedback.

How It Works

Maze Generation

The generator uses recursive backtracking to carve passages through a grid of walls. Starting from a random cell, it randomly chooses unvisited neighboring cells and creates paths between them. When it reaches a dead end, it backtracks to find unexplored paths.

Maze Solving

The solver uses a similar recursive backtracking approach to find a path from the start to the end position. It explores all possible paths until it finds the solution, marking the correct path as it goes.

Technical Details

Mazes are stored as numpy arrays where 1 represents walls and 0 represents passages
Start position is always at (1, 1)
End position is always at (height-2, width-2)
All maze dimensions are odd numbers to ensure proper wall and passage structure
Large mazes are saved as separate .npy files for efficient storage and loading

Performance

The iterative implementation can handle mazes with over 100 million cells
Visualization can be toggled for faster generation of extremely large mazes
Progress tracking provides feedback during long generation times

Output

Generated mazes are saved in the mazes/ directory with timestamps
Each maze file includes metadata such as dimensions, start/end positions, and generation timestamp
Solved mazes are updated with solution paths, step counts, and solve times

Author

Created by Saagnik Mondal

License

This project is open source and available for educational and personal use.
