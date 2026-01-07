import numpy as np
import json
import os
import time
import pygame
import sys
from datetime import datetime


def load_maze(filename, directory="mazes"):
    """
    Load a maze from a JSON file.
    
    Args:
        filename (str): Name of the maze file
        directory (str): Directory containing mazes
    
    Returns:
        tuple: (maze, start_pos, end_pos, maze_data)
    """
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Maze file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    maze = np.array(data['maze'])
    start_pos = tuple(data['start'])
    end_pos = tuple(data['end'])
    
    return maze, start_pos, end_pos, data


def solve_maze_with_pygame(maze, start, end, cell_size=None):
    """
    Solve maze using recursive backtracking with pygame visualization.
    
    Args:
        maze (numpy.ndarray): The maze to solve
        start (tuple): Starting position (y, x)
        end (tuple): Ending position (y, x)
        cell_size (int): Size of each cell in pixels (auto-calculated if None)
    
    Returns:
        tuple: (solution, steps, solve_time)
    """
    pygame.init()
    
    height, width = maze.shape
    
    # Auto-calculate cell size to fit screen if not provided
    if cell_size is None:
        # Get display info for screen size
        display_info = pygame.display.Info()
        max_width = display_info.current_w - 100  # Leave margin
        max_height = display_info.current_h - 200  # Leave margin for info bar
        
        # Calculate cell size to fit the screen
        cell_size_w = max_width // width
        cell_size_h = max_height // height
        cell_size = min(cell_size_w, cell_size_h, 30)  # Max 30 pixels per cell
        cell_size = max(cell_size, 3)  # Minimum 3 pixels per cell
    
    screen_width = width * cell_size
    screen_height = height * cell_size + 60
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Solver - Recursive Backtracking")
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (173, 216, 230)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GRAY = (200, 200, 200)
    
    solution = np.zeros_like(maze)
    visited = np.zeros_like(maze, dtype=bool)
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    start_time = time.time()
    steps = 0
    solved = False
    
    def draw_maze():
        screen.fill(WHITE)
        
        for y in range(height):
            for x in range(width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                
                if (y, x) == start:
                    pygame.draw.rect(screen, GREEN, rect)
                elif (y, x) == end:
                    pygame.draw.rect(screen, RED, rect)
                elif maze[y, x] == 1:
                    pygame.draw.rect(screen, BLACK, rect)
                elif solution[y, x] == 1:
                    pygame.draw.rect(screen, LIGHT_BLUE, rect)
                elif visited[y, x]:
                    pygame.draw.rect(screen, GRAY, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                
                pygame.draw.rect(screen, BLACK, rect, 1)
        
        elapsed_time = time.time() - start_time
        info_text = f"Steps: {steps} | Time: {elapsed_time:.3f}s | Status: {'SOLVED!' if solved else 'Searching...'}"
        text_surface = font.render(info_text, True, BLACK)
        screen.blit(text_surface, (10, screen_height - 50))
        
        pygame.display.flip()
    
    def backtrack(pos):
        nonlocal steps, solved
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        y, x = pos
        
        if pos == end:
            solution[y, x] = 1
            solved = True
            draw_maze()
            return True
        
        if visited[y, x] or maze[y, x] == 1:
            return False
        
        visited[y, x] = True
        solution[y, x] = 1
        steps += 1
        
        if steps % 5 == 0:
            draw_maze()
            clock.tick(60)
        
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dy, dx in moves:
            ny, nx = y + dy, x + dx
            
            if 0 <= ny < height and 0 <= nx < width:
                if backtrack((ny, nx)):
                    return True
        
        solution[y, x] = 0
        return False
    
    draw_maze()
    backtrack(start)
    draw_maze()
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    final_text = f"SOLVED in {solve_time:.3f} seconds with {steps} steps!"
    text_surface = font.render(final_text, True, GREEN)
    screen.blit(text_surface, (10, screen_height - 30))
    pygame.display.flip()
    
    print(f"\n{'='*50}")
    print(f"Maze Solving Results:")
    print(f"{'='*50}")
    print(f"Total Time: {solve_time:.3f} seconds")
    print(f"Total Steps: {steps}")
    print(f"Maze Size: {height}x{width}")
    print(f"{'='*50}\n")
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
        clock.tick(30)
    
    pygame.quit()
    
    return solution, steps, solve_time


def save_solution(filename, solution, steps, solve_time, directory="mazes"):
    """Save the solution back to the maze file."""
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    data['solved'] = True
    data['solution'] = solution.tolist()
    data['steps'] = steps
    data['solve_time'] = solve_time
    data['solved_timestamp'] = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Solution saved to: {filepath}")


def solve_and_save(filename):
    """Load a maze, solve it with pygame visualization, and save the solution."""
    print(f"\n{'='*50}")
    print(f"Loading maze: {filename}")
    print(f"{'='*50}\n")
    
    maze, start, end, maze_data = load_maze(filename)
    
    if maze_data.get('solved'):
        print("This maze has already been solved!")
        print(f"   Previous solve time: {maze_data['solve_time']:.3f}s")
        print(f"   Previous steps: {maze_data['steps']}")
        print("\nSolving again...\n")
    
    print(f"Maze size: {maze.shape}")
    print(f"Start: {start}")
    print(f"End: {end}")
    print("\nLaunching pygame visualization...\n")
    
    solution, steps, solve_time = solve_maze_with_pygame(maze, start, end)
    save_solution(filename, solution, steps, solve_time)
    
    return solution, steps, solve_time


if __name__ == "__main__":
    import glob
    
    # Increase recursion limit for large mazes
    sys.setrecursionlimit(50000)
    
    maze_files = glob.glob("mazes/maze_*.json")
    
    if not maze_files:
        print("No maze files found in 'mazes/' directory")
        print("Run 'python maze.py' to create a maze first")
    else:
        latest_file = max(maze_files, key=os.path.getctime)
        filename = os.path.basename(latest_file)
        solve_and_save(filename)
