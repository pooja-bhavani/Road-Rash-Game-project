import pygame
import random
import os
import sys
import boto3
from pygame.locals import *

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROAD_WIDTH = 400
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 100
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 100
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
ROAD_SPEED = 5
ENEMY_SPEED = 3
OBSTACLE_SPEED = 4
CLOUD_WIDTH = 80
CLOUD_HEIGHT = 40
GRASS_WIDTH = 40
GRASS_HEIGHT = 30
BOARD_WIDTH = 60
BOARD_HEIGHT = 80

# Colors
SKY_BLUE = (135, 206, 235)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Enemy states
PATROL = "patrol"
CHASE = "chase"
ATTACK = "attack"