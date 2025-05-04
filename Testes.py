import numpy as np

# Cria uma maze_matriz 5x5 com zeros
maze_matriz = np.zeros((5, 5), dtype=int)

maze_size = 5  # Must be odd for this generation method
maze_matriz = np.zeros((maze_size, maze_size), dtype=int)
cell = 20

for i in range(maze_size):
    maze_matriz[i, 0] = 1
    maze_matriz[0, i] = 1
    maze_matriz[i, maze_size - 1] = 1
    maze_matriz[maze_size - 1, i] = 1

print(maze_matriz)

for linha in range(maze_size):
    for coluna in range(maze_size):
        x = coluna * cell
        y = linha * cell

        if maze_matriz[linha, coluna] == 1 and coluna % 2 != 0:
            print(linha,coluna, (x, y), (x + cell, y))

        if maze_matriz[linha, coluna] == 1 and coluna % 2 == 0:
            print(linha,coluna, (x, y), (x, y + cell))