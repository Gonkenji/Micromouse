import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Player
player_size = 20
player_x = 50
player_y = 50
player_speed = 5

# Maze generation (simplified recursive backtracker)
def generate_maze(n):
    maze = [[1 for _ in range(n)] for _ in range(n)]  # 1 represents a wall
    def carve_path(x, y):
        maze[y][x] = 0  # 0 represents a path
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and maze[ny][nx] == 1:
                maze[ny - dy // 2][nx - dx // 2] = 0
                carve_path(nx, ny)
    carve_path(1, 1)
    return maze

# Maze parameters
maze_size = 21  # Must be odd for this generation method
maze = generate_maze(maze_size)
cell_size = 20

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_x > 0 and maze[int(player_y // cell_size)][int((player_x - player_speed) // cell_size)] == 