import random
import numpy as np
import json
import os
from datetime import datetime

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

print(f"\n{'='*50}")
print(f"✅ Maze saved to: {filepath}")
print(f"   Size: {HEIGHT}x{WIDTH}")
print(f"   Start: (1, 1)")
print(f"   End: ({HEIGHT - 2}, {WIDTH - 2})")
print(f"\n🎯 Maze ready to be solved!")
print(f"Run: python recursive_backtracking.py")
print(f"{'='*50}\n")