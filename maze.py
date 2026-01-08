import random
import numpy as np
import json
import os
from datetime import datetime
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Note: pygame not available, maze image export disabled")

WIDTH = 39
HEIGHT = 19
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

EMPTY = ' '
MARK = '@'
WALL = chr(9608)
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

maze = {}
for x in range(WIDTH):
    for y in range(HEIGHT):
        maze[(x, y)] = WALL

def printMaze(maze, markX=None, markY=None):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if markX == x and markY == y:
                print(MARK, end='')
            else:
                print(maze[(x, y)], end='')
        print()


def visit(x, y):
    maze[(x, y)] = EMPTY
    printMaze(maze, x, y)
    print('\n\n')

    while True:
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)

        if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)

        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)

        if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        if len(unvisitedNeighbors) == 0:
            return
        else:
            nextIntersection = random.choice(unvisitedNeighbors)

            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = EMPTY
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = EMPTY
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = EMPTY
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = EMPTY

            hasVisited.append((nextX, nextY))
            visit(nextX, nextY)


hasVisited = [(1, 1)]
visit(1, 1)
printMaze(maze)

hasVisited = [(1, 1)]
visit(1, 1)

printMaze(maze)

maze_array = np.zeros((HEIGHT, WIDTH), dtype=int)
for y in range(HEIGHT):
    for x in range(WIDTH):
        if maze[(x, y)] == WALL:
            maze_array[y, x] = 1
        else:
            maze_array[y, x] = 0

if not os.path.exists("mazes"):
    os.makedirs("mazes")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"maze_{timestamp}.json"
filepath = os.path.join("mazes", filename)

data = {
    'maze': maze_array.tolist(),
    'start': [1, 1],
    'end': [HEIGHT - 2, WIDTH - 2],
    'shape': [HEIGHT, WIDTH],
    'timestamp': timestamp,
    'solved': False
}

with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)

image_path = None
if PYGAME_AVAILABLE:
    try:
        image_path = filepath.replace('.json', '.png')
        cell_size = max(10, min(30, 1200 // max(WIDTH, HEIGHT)))
        
        img_width = WIDTH * cell_size
        img_height = HEIGHT * cell_size + 40
        
        pygame.init()
        surface = pygame.Surface((img_width, img_height))
        
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        
        surface.fill(WHITE)
        
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if maze_array[y, x] == 1:
                    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    pygame.draw.rect(surface, BLACK, rect)
        
        start_rect = pygame.Rect(1 * cell_size, 1 * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, GREEN, start_rect)
        
        end_rect = pygame.Rect((WIDTH - 2) * cell_size, (HEIGHT - 2) * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, RED, end_rect)
        
        if cell_size >= 8:
            font = pygame.font.Font(None, min(24, cell_size * 2))
            start_text = font.render('S', True, BLACK)
            end_text = font.render('E', True, BLACK)
            surface.blit(start_text, (1 * cell_size + 2, 1 * cell_size + 2))
            surface.blit(end_text, ((WIDTH - 2) * cell_size + 2, (HEIGHT - 2) * cell_size + 2))
        
        font = pygame.font.Font(None, 24)
        info_text = f"Maze: {WIDTH}x{HEIGHT} | Start (Green) to End (Red)"
        text_surface = font.render(info_text, True, BLACK)
        surface.blit(text_surface, (10, HEIGHT * cell_size + 10))
        
        pygame.image.save(surface, image_path)
        pygame.quit()
    except Exception as e:
        print(f"Could not export image: {e}")
        image_path = None

print(f"\n{'='*50}")
print(f"Maze saved to: {filepath}")
if image_path:
    print(f"Image saved to: {image_path}")
print(f"   Size: {HEIGHT}x{WIDTH}")
print(f"   Start: (1, 1)")
print(f"   End: ({HEIGHT - 2}, {WIDTH - 2})")
print(f"\nMaze ready to be solved!")
print(f"Run: python recursive_backtracking.py")
if image_path:
    print(f"Or open {os.path.basename(image_path)} to solve by hand")
print(f"{'='*50}\n")