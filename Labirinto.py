import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)

# Maze parameters
maze_size = 31  # Must be odd for this generation method
maze_matriz = np.zeros((maze_size, maze_size), dtype=int)
cell = 30

for linhas in range(maze_size):
    for colunas in range(maze_size):
        if linhas % 2 != 0 and colunas % 2 == 0:  #editar verticais
            maze_matriz[linhas, maze_size-1] = 1
            maze_matriz[linhas, 0] = 1
        
        if linhas % 2 == 0 and colunas % 2 != 0: #editar horizontais
            maze_matriz[0, colunas] = 1
            maze_matriz[maze_size -1, colunas] = 1

def generate_maze(maze_size, red, cell):
    for linha in range(maze_size):
        if linha % 2 == 0:
            y = (linha // 2) * cell  # posição horizontal para linhas pares

        for coluna in range(maze_size):
            x = (coluna // 2) * cell  # reinicia x a cada coluna par

            # Paredes horizontais (linha par, coluna ímpar)
            if linha % 2 == 0 and coluna % 2 != 0:
                x += cell  # desloca para início da parede
                if maze_matriz[linha, coluna] == 1:
                    pygame.draw.line(screen, red, (x, y), (x + cell, y))
                    #print(f"Horiz: ({linha},{coluna}) - de ({x},{y}) até ({x + cell},{y})")

            # Paredes verticais (linha ímpar, coluna par)
            elif linha % 2 != 0 and coluna % 2 == 0:
                y_vert = (linha // 2) * cell
                x += cell  # desloca para início da parede
                if maze_matriz[linha, coluna] == 1:
                    pygame.draw.line(screen, red, (x, y_vert), (x, y_vert + cell))
                    #print(f"Vert: ({linha},{coluna}) - de ({x},{y_vert}) até ({x},{y_vert + cell})")
    return


print(maze_matriz)

running = True
k = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if k:
        k = 0
        screen.fill(white)
        generate_maze(maze_size, red, cell)

    pygame.display.flip()

# Quit Pygame
