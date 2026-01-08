import numpy as np
import json
import os
import time
import pygame
import sys
from datetime import datetime


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


def solve_maze_dead_end_filling(maze, start, end, visualize=True):
    height, width = maze.shape
    total_cells = height * width
    
    if total_cells > 10000000:
        print(f"\nWarning: Very large maze ({total_cells:,} cells)")
        print("Solving may take several minutes. Visualization updates reduced to prevent lag.\n")
    
    working_maze = maze.copy()
    solution = np.zeros_like(maze)
    
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
            print(f"Note: Large maze - using 4px cells")
        elif cell_size > 15:
            cell_size = 15
        
        screen_width = min(width * cell_size, max_width)
        screen_height = min(height * cell_size, max_height) + 60
        
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Dead End Filling Solver - {height}x{width} | {cell_size}px cells")
        
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (128, 128, 128)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (100, 149, 237)
        
        font = pygame.font.Font(None, 24)
        clock = pygame.time.Clock()
    
    start_time = time.time()
    iterations = 0
    cells_filled = 0
    
    def count_open_neighbors(y, x):
        count = 0
        neighbors = []
        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                if working_maze[ny, nx] == 0:
                    count += 1
                    neighbors.append((ny, nx))
        return count, neighbors
    
    def draw_maze():
        if not visualize:
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(WHITE)
        
        for y in range(height):
            for x in range(width):
                px = x * cell_size
                py = y * cell_size
                
                if px >= screen_width - cell_size or py >= screen_height - 60:
                    continue
                
                if (y, x) == start:
                    color = GREEN
                elif (y, x) == end:
                    color = RED
                elif working_maze[y, x] == 1:
                    color = BLACK
                elif working_maze[y, x] == 2:
                    color = GRAY
                else:
                    color = WHITE
                
                if cell_size > 1:
                    pygame.draw.rect(screen, color, (px, py, cell_size, cell_size))
                    if cell_size > 2:
                        pygame.draw.rect(screen, (200, 200, 200), (px, py, cell_size, cell_size), 1)
                else:
                    screen.set_at((px, py), color)
        
        elapsed = time.time() - start_time
        info_text = f"Iteration: {iterations} | Filled: {cells_filled} | Time: {elapsed:.2f}s"
        text_surface = font.render(info_text, True, BLACK)
        screen.blit(text_surface, (10, screen_height - 50))
        
        pygame.display.flip()
        
        if total_cells > 1000000:
            clock.tick(120)
        else:
            clock.tick(60)
    
    print("Starting Dead End Filling algorithm...")
    print(f"Maze size: {height}x{width} = {total_cells:,} cells")
    
    if visualize:
        draw_maze()
    
    found_dead_ends = True
    
    while found_dead_ends:
        iterations += 1
        found_dead_ends = False
        dead_ends = []
        
        for y in range(height):
            for x in range(width):
                if working_maze[y, x] == 0 and (y, x) != start and (y, x) != end:
                    open_count, neighbors = count_open_neighbors(y, x)
                    if open_count == 1:
                        dead_ends.append((y, x))
        
        if dead_ends:
            found_dead_ends = True
            cells_filled += len(dead_ends)
            
            for y, x in dead_ends:
                working_maze[y, x] = 2
            
            if total_cells > 10000000:
                update_freq = 10
            elif total_cells > 1000000:
                update_freq = 5
            else:
                update_freq = 1
            
            if visualize and iterations % update_freq == 0:
                draw_maze()
            
            if iterations % 10 == 0:
                print(f"Iteration {iterations}: Filled {len(dead_ends)} dead ends (Total: {cells_filled})")
    
    for y in range(height):
        for x in range(width):
            if working_maze[y, x] == 0:
                solution[y, x] = 1
    
    end_time = time.time()
    solve_time = end_time - start_time
    
    print(f"\nDead End Filling Complete!")
    print(f"Total iterations: {iterations}")
    print(f"Dead ends filled: {cells_filled}")
    print(f"Solution path cells: {np.sum(solution)}")
    print(f"Solve time: {solve_time:.2f} seconds")
    
    if visualize:
        for y in range(height):
            for x in range(width):
                if solution[y, x] == 1:
                    working_maze[y, x] = 0
                elif working_maze[y, x] == 2:
                    working_maze[y, x] = 1
        
        screen.fill(WHITE)
        
        for y in range(height):
            for x in range(width):
                px = x * cell_size
                py = y * cell_size
                
                if px >= screen_width - cell_size or py >= screen_height - 60:
                    continue
                
                if (y, x) == start:
                    color = GREEN
                elif (y, x) == end:
                    color = RED
                elif working_maze[y, x] == 1:
                    color = BLACK
                elif solution[y, x] == 1:
                    color = BLUE
                else:
                    color = WHITE
                
                if cell_size > 1:
                    pygame.draw.rect(screen, color, (px, py, cell_size, cell_size))
                    if cell_size > 2:
                        pygame.draw.rect(screen, (200, 200, 200), (px, py, cell_size, cell_size), 1)
                else:
                    screen.set_at((px, py), color)
        
        final_text = f"SOLVED! Time: {solve_time:.2f}s | Path: {np.sum(solution)} cells"
        text_surface = font.render(final_text, True, (0, 128, 0))
        screen.blit(text_surface, (10, screen_height - 50))
        
        pygame.display.flip()
        
        print("\nClose window to exit...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            clock.tick(30)
        
        pygame.quit()
    
    return solution, cells_filled, solve_time


def save_solution(filename, solution, stats, solve_time, directory="mazes"):
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    data['solved'] = True
    data['solution'] = solution.tolist()
    data['algorithm'] = 'dead_end_filling'
    data['dead_ends_filled'] = int(stats)
    data['solution_path_length'] = int(np.sum(solution))
    data['solve_time'] = solve_time
    data['solved_timestamp'] = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nSolution saved to: {filepath}")


def export_solution_image(maze, solution, start, end, filename):
    height, width = maze.shape
    total_cells = height * width
    
    if total_cells > 10000000:
        cell_size = 5
    elif total_cells > 4000000:
        cell_size = 8
    elif total_cells > 1000000:
        cell_size = 12
    elif total_cells > 100000:
        cell_size = 15
    else:
        cell_size = 20
    
    img_width = width * cell_size
    img_height = height * cell_size + 40
    
    max_dim = 32767
    if img_width > max_dim or img_height > max_dim:
        cell_size = max(1, min(max_dim // width, max_dim // height))
        img_width = width * cell_size
        img_height = height * cell_size + 40
    
    try:
        pygame.init()
        surface = pygame.Surface((img_width, img_height))
        
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (100, 149, 237)
        
        surface.fill(WHITE)
        
        print(f"Rendering solution image ({width}x{height})...")
        for y in range(height):
            for x in range(width):
                if maze[y, x] == 1:
                    color = BLACK
                elif solution[y, x] == 1:
                    color = BLUE
                else:
                    color = WHITE
                
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, color, rect)
        
        start_y, start_x = start
        start_rect = pygame.Rect(start_x * cell_size, start_y * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, GREEN, start_rect)
        
        end_y, end_x = end
        end_rect = pygame.Rect(end_x * cell_size, end_y * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, RED, end_rect)
        
        if cell_size >= 8:
            font = pygame.font.Font(None, min(24, cell_size * 2))
            start_text = font.render('S', True, BLACK)
            end_text = font.render('E', True, BLACK)
            surface.blit(start_text, (start_x * cell_size + 2, start_y * cell_size + 2))
            surface.blit(end_text, (end_x * cell_size + 2, end_y * cell_size + 2))
        
        font = pygame.font.Font(None, 24)
        info_text = f"Solved: {width}x{height} | Solution Path (Blue) | Dead End Filling Algorithm"
        text_surface = font.render(info_text, True, BLACK)
        surface.blit(text_surface, (10, height * cell_size + 10))
        
        output_path = filename.replace('.json', '_solution.png')
        pygame.image.save(surface, output_path)
        pygame.quit()
        
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Solution image saved: {output_path} ({file_size:.2f} MB)")
        
        return output_path
        
    except Exception as e:
        print(f"Error exporting solution image: {e}")
        return None


def solve_and_save(filename, visualize=True, export_image=True):
    print(f"\n{'='*60}")
    print(f"Loading maze: {filename}")
    print(f"{'='*60}\n")
    
    maze, start, end, maze_data = load_maze(filename)
    
    if maze_data.get('solved'):
        print("This maze has already been solved!")
        if maze_data.get('algorithm') == 'dead_end_filling':
            print(f"   Previous solve time: {maze_data['solve_time']:.2f}s")
            print(f"   Dead ends filled: {maze_data.get('dead_ends_filled', 'N/A')}")
        print("\nSolving again with Dead End Filling...\n")
    
    solution, stats, solve_time = solve_maze_dead_end_filling(
        maze, start, end, visualize=visualize
    )
    
    save_solution(filename, solution, stats, solve_time)
    
    if export_image:
        filepath = os.path.join("mazes", filename)
        export_solution_image(maze, solution, start, end, filepath)
    
    return solution, stats, solve_time


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
        print("DEAD END FILLING MAZE SOLVER")
        print("="*60)
        print("\nThis algorithm fills in all dead ends until only")
        print("the solution path remains.\n")
        
        visualize = input("Enable visualization? (y/n, default=y): ").strip().lower() != 'n'
        export_image = input("Export solution as image? (y/n, default=y): ").strip().lower() != 'n'
        
        solve_and_save(filename, visualize=visualize, export_image=export_image)
