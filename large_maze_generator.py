import random
import numpy as np
import json
import os
import sys
from datetime import datetime
import pygame
from collections import deque

class LargeMazeGenerator:
    def __init__(self, width, height):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        
        self.WIDTH = width
        self.HEIGHT = height
        self.total_cells = width * height
        
        print(f"Initializing maze generator: {width}x{height} = {self.total_cells:,} cells")
        
        self.WALL = 1
        self.EMPTY = 0
        self.NORTH, self.SOUTH, self.EAST, self.WEST = 0, 1, 2, 3
        
        sys.setrecursionlimit(min(100000, max(1000, self.total_cells // 100)))
        
    def generate_iterative(self, visualize=True, cell_size=1):
        print("Generating maze using iterative backtracking...")
        
        maze = np.ones((self.HEIGHT, self.WIDTH), dtype=np.uint8)
        
        stack = [(1, 1)]
        visited = set()
        visited.add((1, 1))
        maze[1, 1] = self.EMPTY
        
        total_passages = ((self.HEIGHT // 2) * (self.WIDTH // 2))
        progress_interval = max(1, total_passages // 100)
        
        screen = None
        if visualize and self.total_cells <= 10000000:
            pygame.init()
            
            max_screen_width = 1920
            max_screen_height = 1080
            
            scale_w = max_screen_width // self.WIDTH
            scale_h = max_screen_height // self.HEIGHT
            cell_size = max(1, min(scale_w, scale_h, cell_size))
            
            screen_width = min(self.WIDTH * cell_size, max_screen_width)
            screen_height = min(self.HEIGHT * cell_size, max_screen_height)
            
            screen = pygame.display.set_mode((screen_width, screen_height + 50))
            pygame.display.set_caption(f"Generating Maze: {self.WIDTH}x{self.HEIGHT}")
            
            BLACK = (0, 0, 0)
            WHITE = (255, 255, 255)
            BLUE = (100, 149, 237)
            font = pygame.font.Font(None, 24)
        
        step = 0
        
        while stack:
            for event in pygame.event.get() if screen else []:
                if event.type == pygame.QUIT:
                    if screen:
                        pygame.quit()
                    sys.exit()
            
            x, y = stack[-1]
            
            neighbors = []
            directions = [
                (0, -2, self.NORTH),
                (0, 2, self.SOUTH),
                (-2, 0, self.WEST),
                (2, 0, self.EAST)
            ]
            
            for dx, dy, direction in directions:
                nx, ny = x + dx, y + dy
                if (0 < nx < self.WIDTH - 1 and 
                    0 < ny < self.HEIGHT - 1 and 
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                
                maze[y + dy // 2, x + dx // 2] = self.EMPTY
                maze[ny, nx] = self.EMPTY
                
                visited.add((nx, ny))
                stack.append((nx, ny))
                
                step += 1
                
                if screen and step % progress_interval == 0:
                    screen.fill(BLACK)
                    
                    for sy in range(0, self.HEIGHT, max(1, self.HEIGHT // screen_height)):
                        for sx in range(0, self.WIDTH, max(1, self.WIDTH // screen_width)):
                            if maze[sy, sx] == self.EMPTY:
                                px = (sx * cell_size) % screen_width
                                py = (sy * cell_size) % screen_height
                                if cell_size > 1:
                                    pygame.draw.rect(screen, WHITE, (px, py, cell_size, cell_size))
                                else:
                                    screen.set_at((px, py), WHITE)
                    
                    progress = (len(visited) / total_passages) * 100
                    text = font.render(f"Progress: {progress:.1f}% ({len(visited):,}/{total_passages:,})", True, BLUE)
                    screen.blit(text, (10, screen_height + 10))
                    
                    pygame.display.flip()
                
                if step % 10000 == 0:
                    progress = (len(visited) / total_passages) * 100
                    print(f"Progress: {progress:.1f}% - Visited: {len(visited):,}/{total_passages:,}")
            else:
                stack.pop()
        
        if screen:
            screen.fill(BLACK)
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if maze[y, x] == self.EMPTY:
                        px = x * cell_size
                        py = y * cell_size
                        if px < screen_width and py < screen_height:
                            if cell_size > 1:
                                pygame.draw.rect(screen, WHITE, (px, py, cell_size, cell_size))
                            else:
                                screen.set_at((px, py), WHITE)
            
            text = font.render(f"Maze Complete! {self.WIDTH}x{self.HEIGHT}", True, (0, 255, 0))
            screen.blit(text, (10, screen_height + 10))
            pygame.display.flip()
            
            print("\nMaze generated! Close the window to continue...")
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        pygame.time.wait(100)
            
            pygame.quit()
        
        print(f"Maze generation complete! Total passages: {len(visited):,}")
        return maze
    
    def save_maze(self, maze, filename=None):
        if not os.path.exists("mazes"):
            os.makedirs("mazes")
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"maze_{self.WIDTH}x{self.HEIGHT}_{timestamp}.json"
        
        filepath = os.path.join("mazes", filename)
        
        data = {
            'width': int(self.WIDTH),
            'height': int(self.HEIGHT),
            'total_cells': int(self.total_cells),
            'start': [1, 1],
            'end': [int(self.HEIGHT - 2), int(self.WIDTH - 2)],
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'solved': False
        }
        
        if self.total_cells <= 100000000:
            data['maze'] = maze.tolist()
            print(f"Saving full maze data...")
        else:
            print(f"Maze too large ({self.total_cells:,} cells) - saving metadata only")
            np.save(filepath.replace('.json', '.npy'), maze)
            data['maze_file'] = filename.replace('.json', '.npy')
            data['note'] = 'Full maze data saved in separate .npy file'
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✅ Maze saved to: {filepath}")
        print(f"   Size: {self.HEIGHT}x{self.WIDTH} = {self.total_cells:,} cells")
        print(f"   Start: (1, 1)")
        print(f"   End: ({self.HEIGHT - 2}, {self.WIDTH - 2})")
        print(f"{'='*60}\n")
        
        return filepath
    
    def visualize_maze(self, maze, cell_size=1):
        pygame.init()
        
        max_screen_width = 1920
        max_screen_height = 1080
        
        scale_w = max_screen_width // self.WIDTH
        scale_h = max_screen_height // self.HEIGHT
        cell_size = max(1, min(scale_w, scale_h, cell_size))
        
        screen_width = min(self.WIDTH * cell_size, max_screen_width)
        screen_height = min(self.HEIGHT * cell_size, max_screen_height)
        
        screen = pygame.display.set_mode((screen_width, screen_height + 50))
        pygame.display.set_caption(f"Maze: {self.WIDTH}x{self.HEIGHT} ({self.total_cells:,} cells)")
        
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        font = pygame.font.Font(None, 24)
        
        screen.fill(BLACK)
        
        print("Rendering maze...")
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                px = x * cell_size
                py = y * cell_size
                
                if px < screen_width and py < screen_height:
                    color = WHITE if maze[y, x] == self.EMPTY else BLACK
                    
                    if (y, x) == (1, 1):
                        color = GREEN
                    elif (y, x) == (self.HEIGHT - 2, self.WIDTH - 2):
                        color = RED
                    
                    if cell_size > 1:
                        pygame.draw.rect(screen, color, (px, py, cell_size, cell_size))
                    else:
                        screen.set_at((px, py), color)
        
        text = font.render(f"Maze: {self.WIDTH}x{self.HEIGHT} ({self.total_cells:,} cells)", True, WHITE)
        screen.blit(text, (10, screen_height + 10))
        
        pygame.display.flip()
        print("Maze rendered! Close window to exit...")
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        
        pygame.quit()


def main():
    print("="*60)
    print("LARGE MAZE GENERATOR")
    print("="*60)
    print("\nThis generator can create mazes with 30+ million cells")
    print("and visualize them in real-time using pygame.\n")
    
    presets = {
        '1': (5001, 5001, "Small (~25M cells)"),
        '2': (7001, 7001, "Medium (~49M cells)"),
        '3': (10001, 10001, "Large (~100M cells)"),
        '4': (6001, 9001, "Wide (~54M cells)"),
        '5': (9001, 6001, "Tall (~54M cells)"),
    }
    
    print("Preset sizes:")
    for key, (w, h, desc) in presets.items():
        print(f"  {key}. {desc}: {w}x{h} = {w*h:,} cells")
    
    print("  c. Custom size")
    
    choice = input("\nSelect preset (1-5) or 'c' for custom: ").strip().lower()
    
    if choice in presets:
        width, height, _ = presets[choice]
    elif choice == 'c':
        width = int(input("Enter width (odd number, e.g., 5001): "))
        height = int(input("Enter height (odd number, e.g., 5001): "))
    else:
        print("Invalid choice. Using default: 5001x5001")
        width, height = 5001, 5001
    
    visualize = input("\nVisualize during generation? (y/n, default=y): ").strip().lower() != 'n'
    
    generator = LargeMazeGenerator(width, height)
    
    print(f"\nGenerating {width}x{height} maze ({generator.total_cells:,} cells)...")
    print("This may take several minutes for very large mazes...\n")
    
    import time
    start_time = time.time()
    
    maze = generator.generate_iterative(visualize=visualize)
    
    elapsed = time.time() - start_time
    print(f"\nGeneration time: {elapsed:.2f} seconds")
    
    generator.save_maze(maze)
    
    view = input("\nView final maze? (y/n): ").strip().lower()
    if view == 'y':
        generator.visualize_maze(maze)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
