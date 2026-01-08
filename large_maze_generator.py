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
        
        # Not using recursion for generation, but set reasonable limit for safety
        sys.setrecursionlimit(10000)
        
    def generate_iterative(self, visualize=True, cell_size=1):
        print("Generating maze using iterative backtracking...")
        
        maze = np.ones((self.HEIGHT, self.WIDTH), dtype=np.uint8)
        
        stack = [(1, 1)]
        visited = set()
        visited.add((1, 1))
        maze[1, 1] = self.EMPTY
        
        total_passages = ((self.HEIGHT // 2) * (self.WIDTH // 2))
        
        # Optimize progress updates based on maze size
        if self.total_cells > 10000000:
            progress_interval = max(10000, total_passages // 20)
        elif self.total_cells > 1000000:
            progress_interval = max(5000, total_passages // 50)
        else:
            progress_interval = max(100, total_passages // 100)
        
        screen = None
        if visualize and self.total_cells <= 4000000:
            pygame.init()
            
            display_info = pygame.display.Info()
            max_screen_width = display_info.current_w - 150
            max_screen_height = display_info.current_h - 250
            
            scale_w = max_screen_width // self.WIDTH
            scale_h = max_screen_height // self.HEIGHT
            cell_size = min(scale_w, scale_h)
            
            # Balance between visibility and fitting on screen
            if cell_size < 4:
                cell_size = 4
                print(f"Note: Large maze - using 4px cells")
            elif cell_size > 15:
                cell_size = 15
                print(f"Note: Using 15px cells for optimal visibility")
            
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
                    
                    # Optimize rendering for large mazes - sample pixels
                    sample_rate = max(1, self.HEIGHT // 800, self.WIDTH // 800)
                    for sy in range(0, self.HEIGHT, sample_rate):
                        for sx in range(0, self.WIDTH, sample_rate):
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
                    pygame.time.wait(10)  # Small delay to prevent CPU overload
                
                if self.total_cells > 10000000:
                    if step % 50000 == 0:
                        progress = (len(visited) / total_passages) * 100
                        print(f"Progress: {progress:.1f}% - Visited: {len(visited):,}/{total_passages:,}")
                elif step % 10000 == 0:
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
        
        image_path = self.export_as_image(maze, filepath.replace('.json', '.png'))
        if image_path:
            print(f"   Image: {image_path}")
        
        print(f"{'='*60}\n")
        
        return filepath
    
    def export_as_image(self, maze, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"maze_{self.WIDTH}x{self.HEIGHT}_{timestamp}.png"
        
        if not filename.startswith('mazes/'):
            filename = os.path.join('mazes', os.path.basename(filename))
        
        print(f"Exporting maze as image for manual solving...")
        
        cell_size = 1
        if self.total_cells > 10000000:
            print(f"Maze too large to export as single image ({self.total_cells:,} cells)")
            return None
        elif self.total_cells > 4000000:
            cell_size = 5
            print(f"Creating large image with {cell_size}px per cell (may take time)...")
        elif self.total_cells > 1000000:
            cell_size = 8
        elif self.total_cells > 100000:
            cell_size = 12
        else:
            cell_size = 20
        
        img_width = self.WIDTH * cell_size
        img_height = self.HEIGHT * cell_size + 40
        
        if img_width > 32767 or img_height > 32767:
            print(f"Image dimensions too large ({img_width}x{img_height}), reducing cell size...")
            cell_size = max(1, min(32767 // self.WIDTH, 32767 // self.HEIGHT))
            img_width = self.WIDTH * cell_size
            img_height = self.HEIGHT * cell_size + 40
        
        try:
            pygame.init()
            surface = pygame.Surface((img_width, img_height))
            
            BLACK = (0, 0, 0)
            WHITE = (255, 255, 255)
            GREEN = (0, 255, 0)
            RED = (255, 0, 0)
            
            surface.fill(WHITE)
            
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if maze[y, x] == self.WALL:
                        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                        pygame.draw.rect(surface, BLACK, rect)
            
            start_rect = pygame.Rect(1 * cell_size, 1 * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, GREEN, start_rect)
            
            end_rect = pygame.Rect((self.WIDTH - 2) * cell_size, (self.HEIGHT - 2) * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, RED, end_rect)
            
            if cell_size >= 8:
                font = pygame.font.Font(None, min(24, cell_size * 2))
                start_text = font.render('S', True, BLACK)
                end_text = font.render('E', True, BLACK)
                surface.blit(start_text, (1 * cell_size + 2, 1 * cell_size + 2))
                surface.blit(end_text, ((self.WIDTH - 2) * cell_size + 2, (self.HEIGHT - 2) * cell_size + 2))
            
            font = pygame.font.Font(None, 24)
            info_text = f"Maze: {self.WIDTH}x{self.HEIGHT} | Start (Green) to End (Red)"
            text_surface = font.render(info_text, True, BLACK)
            surface.blit(text_surface, (10, self.HEIGHT * cell_size + 10))
            
            pygame.image.save(surface, filename)
            pygame.quit()
            
            file_size = os.path.getsize(filename) / (1024 * 1024)
            print(f"✅ Image exported: {file_size:.2f} MB")
            
            return filename
            
        except Exception as e:
            print(f"Error exporting image: {e}")
            return None
    
    def visualize_maze(self, maze, cell_size=None):
        pygame.init()
        
        display_info = pygame.display.Info()
        max_screen_width = display_info.current_w - 150
        max_screen_height = display_info.current_h - 250
        
        if cell_size is None:
            scale_w = max_screen_width // self.WIDTH
            scale_h = max_screen_height // self.HEIGHT
            cell_size = min(scale_w, scale_h)
            
            # Balance visibility and fitting on screen
            if cell_size < 4:
                cell_size = 4
                print(f"Note: Large maze - using 4px cells")
            elif cell_size > 15:
                cell_size = 15
        
        screen_width = min(self.WIDTH * cell_size, max_screen_width)
        screen_height = min(self.HEIGHT * cell_size, max_screen_height) + 50
        
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(f"Maze: {self.WIDTH}x{self.HEIGHT} ({self.total_cells:,} cells) | {cell_size}px cells")
        
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
    print("\nOptimized for Mac M1 Air 8GB - Max 50M cells")
    print("Large mazes (>10M cells) disable visualization to prevent lag\n")
    
    presets = {
        '1': (201, 201, "Small (40K cells) - Very visible"),
        '2': (501, 501, "Medium (251K cells) - Recommended"),
        '3': (1001, 1001, "Large (1M cells) - Good balance"),
        '4': (2001, 2001, "Extra Large (4M cells) - Advanced"),
        '5': (5001, 5001, "Huge (25M cells) - Expert only"),
        '6': (7001, 7001, "Maximum (49M cells) - Visualization disabled"),
    }
    
    print("Preset sizes:")
    for key, (w, h, desc) in presets.items():
        print(f"  {key}. {desc}: {w}x{h} = {w*h:,} cells")
    
    print("  c. Custom size")
    print("\nRecommended for 8GB RAM: Options 1-3")
    
    choice = input("\nSelect preset (1-5) or 'c' for custom: ").strip().lower()
    
    if choice in presets:
        width, height, _ = presets[choice]
    elif choice == 'c':
        width = int(input("Enter width (odd number, e.g., 5001): "))
        height = int(input("Enter height (odd number, e.g., 5001): "))
    else:
        print("Invalid choice. Using default: 5001x5001")
        width, height = 5001, 5001
    
    # Auto-disable visualization for very large mazes to prevent lag
    if width * height > 10000000:
        print(f"\n⚠️  Warning: Maze is very large ({width * height:,} cells)")
        print("Visualization automatically disabled to prevent lag.")
        print("Generation will take several minutes. Please be patient...")
        visualize = False
    else:
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
