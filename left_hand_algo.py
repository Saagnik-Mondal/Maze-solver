import numpy as np 
import json
import os 
import time 
import pygame 
import sys 
from datetime import datetime


# Color constants for visualization
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 200, 0)
COLOR_RED = (200, 0, 0)
COLOR_BLUE = (80, 120, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GRAY = (128, 128, 128)


def load_maze(filename, directory="mazes"):
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Maze file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    if 'maze' in data:
        maze = np.array(data['maze'])
    elif 'maze_file' in data:
        npy_path = os.path.join(directory, data['maze_file'])
        maze = np.load(npy_path)
    else:
        raise ValueError("No maze data found in file")
    
    start_pos = tuple(data['start'])
    end_pos = tuple(data['end'])
    
    return maze, start_pos, end_pos, data


def left_hand_algo(maze, start, end, visualize = True, max_steps = 10000000):
    if maze is None or len(maze.shape) != 2:
        raise ValueError("Invalid maze: must be a 2D numpy array")
    
    if not (0 <= start[0] < maze.shape[0] and 0 <= start[1] < maze.shape[1]):
        raise ValueError(f"Start position {start} is out of bounds")
    
    if not (0 <= end[0] < maze.shape[0] and 0 <= end[1] < maze.shape[1]):
        raise ValueError(f"End position {end} is out of bounds")
    
    height, width = maze.shape
    solution = np.zeros_like(maze)
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    DIR_NAMES = ["UP", "RIGHT", "DOWN", "LEFT"]

    def in_bounds(y, x):
        return 0 <= y < height and 0 <= x < width

    def is_open(y, x):
        return in_bounds(y, x) and maze[y, x] == 0

    # Initial direction: pick first open neighbor
    y, x = start
    direction = None
    for d, (dy, dx) in enumerate(DIRS):
        if is_open(y + dy, x + dx):
            direction = d
            break

    if direction is None:
        raise RuntimeError("Start position is enclosed. Left-hand rule cannot begin.")

    if visualize:
        pygame.init()
        
        display_info = pygame.display.Info()
        max_width = display_info.current_w - 150
        max_height = display_info.current_h - 250
        
        cell_size_w = max_width // width
        cell_size_h = max_height // height
        cell_size = min(cell_size_w, cell_size_h)
        
        if cell_size < 4:
            cell_size = 4
        elif cell_size > 15:
            cell_size = 15
        
        screen_width = min(width * cell_size, max_width)
        screen_height = min(height * cell_size, max_height) + 60
        
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Left-Hand Rule Solver - {height}x{width} | {cell_size}px cells")

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (0, 200, 0)
        RED = (200, 0, 0)
        BLUE = (80, 120, 255)
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24)

    start_time = time.time()
    steps = 0
    path = []
    backtracks = 0
    turns_made = {'left': 0, 'forward': 0, 'right': 0, 'back': 0}
    
    prev_direction = direction

    while (y, x) != end:
        steps += 1
        if steps > max_steps:
            raise RuntimeError("Left-hand rule exceeded step limit. Likely looping maze.")

        # Left, forward, right, back
        for turn in [-1, 0, 1, 2]:
            ndir = (direction + turn) % 4
            dy, dx = DIRS[ndir]
            ny, nx = y + dy, x + dx
            if is_open(ny, nx):
                direction = ndir
                y, x = ny, nx
                break

        solution[y, x] = 1
        path.append((y, x))

        if visualize and steps % 2 == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(WHITE)
            for iy in range(height):
                for ix in range(width):
                    px = ix * cell_size
                    py = iy * cell_size
                    
                    if px >= screen_width - cell_size or py >= screen_height - 60:
                        continue
                    
                    color = WHITE
                    if maze[iy, ix] == 1:
                        color = BLACK
                    if solution[iy, ix] == 1:
                        color = BLUE
                    if (iy, ix) == start:
                        color = GREEN
                    if (iy, ix) == end:
                        color = RED
                    pygame.draw.rect(
                        screen,
                        color,
                        (px, py, cell_size, cell_size),
                    )
            
            elapsed = time.time() - start_time
            info_text = f"Steps: {steps} | Path length: {len(path)} | Time: {elapsed:.2f}s"
            text_surface = font.render(info_text, True, BLACK)
            screen.blit(text_surface, (10, screen_height - 50))

            pygame.display.flip()
            clock.tick(120)

    end_time = time.time()
    solve_time = end_time - start_time
    
    print(f"\nLeft-Hand Rule Complete!")
    print(f"Total steps: {steps}")
    print(f"Path length: {len(path)}")
    print(f"Solve time: {solve_time:.2f} seconds")
    
    if visualize:
        screen.fill(WHITE)
        for iy in range(height):
            for ix in range(width):
                px = ix * cell_size
                py = iy * cell_size
                
                if px >= screen_width - cell_size or py >= screen_height - 60:
                    continue
                
                color = WHITE
                if maze[iy, ix] == 1:
                    color = BLACK
                if solution[iy, ix] == 1:
                    color = BLUE
                if (iy, ix) == start:
                    color = GREEN
                if (iy, ix) == end:
                    color = RED
                pygame.draw.rect(
                    screen,
                    color,
                    (px, py, cell_size, cell_size),
                )
        
        final_text = f"SOLVED! Time: {solve_time:.2f}s | Path: {len(path)} cells"
        text_surface = font.render(final_text, True, (0, 128, 0))
        screen.blit(text_surface, (10, screen_height - 50))
        pygame.display.flip()
        
        print("Solved. Close window to exit.")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            clock.tick(30)
        pygame.quit()

    return solution, steps, solve_time


def save_solution(filename, solution, steps, solve_time, directory="mazes"):
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    data['solved'] = True
    data['solution'] = solution.tolist()
    data['algorithm'] = 'left_hand_rule'
    data['steps'] = int(steps)
    data['solution_path_length'] = int(np.sum(solution))
    data['solve_time'] = solve_time
    data['solved_timestamp'] = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nSolution saved to: {filepath}")


def solve_and_save(filename, visualize=True):
    print(f"\n{'='*60}")
    print(f"Loading maze: {filename}")
    print(f"{'='*60}\n")
    
    maze, start, end, maze_data = load_maze(filename)
    
    if maze_data.get('solved'):
        print("This maze has already been solved!")
        if maze_data.get('algorithm') == 'left_hand_rule':
            print(f"   Previous solve time: {maze_data['solve_time']:.2f}s")
            print(f"   Previous steps: {maze_data.get('steps', 'N/A')}")
        print("\nSolving again with Left-Hand Rule...\n")
    
    print(f"Maze size: {maze.shape}")
    print(f"Start: {start}")
    print(f"End: {end}")
    print("\nLaunching solver...\n")
    
    solution, steps, solve_time = left_hand_algo(maze, start, end, visualize=visualize)
    save_solution(filename, solution, steps, solve_time)
    
    return solution, steps, solve_time


if __name__ == "__main__":
    import glob
    
    maze_files = glob.glob("mazes/maze_*.json")
    
    if not maze_files:
        print("No maze files found in 'mazes/' directory")
        print("Run 'python maze.py' to create a maze first")
    else:
        latest_file = max(maze_files, key=os.path.getctime)
        filename = os.path.basename(latest_file)
        
        print("\n" + "="*60)
        print("LEFT-HAND RULE MAZE SOLVER")
        print("="*60)
        print("\nThis algorithm follows the left wall until reaching the exit.")
        print("Works best on simply-connected mazes.\n")
        
        visualize = input("Enable visualization? (y/n, default=y): ").strip().lower() != 'n'
        
        solve_and_save(filename, visualize=visualize)