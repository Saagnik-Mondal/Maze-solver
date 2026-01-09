import numpy as np 
import json
import os 
import time 
import pygame 
import sys 
from datetime import datetime

def left_hand_algo(maze, start, end, vizulize = True, max_steps = 10000000):
    height, width = maze.shape
    solution = np.zeros_like(maze)