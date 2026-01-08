import numpy as np
import json
import os
import pygame
from datetime import datetime

def load_maze_from_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    if 'maze' in data:
        maze = np.array(data['maze'], dtype=np.uint8)
    elif 'maze_file' in data:
        npy_path = os.path.join(os.path.dirname(filepath), data['maze_file'])
        maze = np.load(npy_path)
    else:
        raise ValueError("No maze data found in file")
    
    return maze, data

def export_maze_to_image(maze, output_path, start=(1, 1), end=None):
    height, width = maze.shape
    
    if end is None:
        end = (height - 2, width - 2)
    
    print(f"Exporting {width}x{height} maze to image...")
    
    total_cells = width * height
    
    if total_cells > 10000000:
        print(f"Warning: Maze too large ({total_cells:,} cells). Using 5px cells - image will be very large!")
        cell_size = 5
    elif total_cells > 4000000:
        cell_size = 8
    elif total_cells > 1000000:
        cell_size = 12
    elif total_cells > 100000:
        cell_size = 15
    elif total_cells > 10000:
        cell_size = 20
    else:
        cell_size = 25
    
    img_width = width * cell_size
    img_height = height * cell_size + 40
    
    max_dim = 32767
    if img_width > max_dim or img_height > max_dim:
        cell_size = max(1, min(max_dim // width, max_dim // height))
        img_width = width * cell_size
        img_height = height * cell_size + 40
    
    pygame.init()
    surface = pygame.Surface((img_width, img_height))
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    surface.fill(WHITE)
    
    print("Rendering maze...")
    for y in range(height):
        for x in range(width):
            if maze[y, x] == 1:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(surface, BLACK, rect)
    
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
    info_text = f"Maze: {width}x{height} ({total_cells:,} cells) | Start (Green) to End (Red)"
    text_surface = font.render(info_text, True, BLACK)
    surface.blit(text_surface, (10, height * cell_size + 10))
    
    pygame.image.save(surface, output_path)
    pygame.quit()
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Image saved: {output_path}")
    print(f"File size: {file_size:.2f} MB")
    print(f"Dimensions: {img_width}x{img_height} pixels")
    print(f"Cell size: {cell_size}px")
    
    return output_path

def main():
    import glob
    
    print("="*60)
    print("MAZE IMAGE EXPORTER")
    print("="*60)
    print("\nThis tool exports maze files as PNG images for manual solving.\n")
    
    maze_files = glob.glob("mazes/maze_*.json")
    
    if not maze_files:
        print("No maze files found in mazes/ directory")
        print("Generate a maze first using maze.py or large_maze_generator.py")
        return
    
    maze_files.sort(key=os.path.getmtime, reverse=True)
    
    print("Available mazes:")
    for i, filepath in enumerate(maze_files[:10], 1):
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            size_info = f"{data.get('width', '?')}x{data.get('height', '?')}"
            total = data.get('total_cells', data.get('width', 0) * data.get('height', 0))
            print(f"  {i}. {filename} ({size_info}, {total:,} cells)")
        except:
            print(f"  {i}. {filename}")
    
    if len(maze_files) > 10:
        print(f"  ... and {len(maze_files) - 10} more")
    
    choice = input("\nSelect maze number (or press Enter for latest): ").strip()
    
    if choice == "":
        selected_file = maze_files[0]
    elif choice.isdigit() and 1 <= int(choice) <= min(10, len(maze_files)):
        selected_file = maze_files[int(choice) - 1]
    else:
        print("Invalid choice. Using latest maze.")
        selected_file = maze_files[0]
    
    print(f"\nLoading: {os.path.basename(selected_file)}")
    
    try:
        maze, data = load_maze_from_file(selected_file)
        
        start = tuple(data.get('start', [1, 1]))
        end = tuple(data.get('end', [maze.shape[0] - 2, maze.shape[1] - 2]))
        
        output_path = selected_file.replace('.json', '.png')
        
        export_maze_to_image(maze, output_path, start, end)
        
        print(f"\nMaze exported successfully!")
        print(f"You can now view and print {os.path.basename(output_path)}")
        print(f"to solve it by hand.")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
