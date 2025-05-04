import random

SIZE = 16
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
DIR_OFFSETS = {
    NORTH: (-1, 0),
    EAST:  (0, 1),
    SOUTH: (1, 0),
    WEST:  (0, -1)
}
DIR_NAMES = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
OPPOSITE = {0: 2, 1: 3, 2: 0, 3: 1}

class Cell:
    def __init__(self):
        self.walls = [True, True, True, True]  # N, E, S, W
        self.visited = False

maze = [[Cell() for _ in range(SIZE)] for _ in range(SIZE)]

def dfs(x, y):
    maze[x][y].visited = True
    dirs = [0, 1, 2, 3]
    random.shuffle(dirs)
    for d in dirs:
        dx, dy = DIR_OFFSETS[d]
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and not maze[nx][ny].visited:
            maze[x][y].walls[d] = False
            maze[nx][ny].walls[OPPOSITE[d]] = False
            dfs(nx, ny)

# Começa em uma célula aleatória
dfs(random.randint(0, SIZE - 1), random.randint(0, SIZE - 1))

# Gera lista de paredes restantes
wall_list = []
for x in range(SIZE):
    for y in range(SIZE):
        for d in range(4):
            if maze[x][y].walls[d]:
                wall_list.append((x, y, DIR_NAMES[d]))

# Remove duplicatas (parede entre duas células aparece 2 vezes)
unique_walls = set()
for (x, y, dir) in wall_list:
    if dir == 'N' and x > 0:
        pair = tuple(sorted([(x, y, 'N'), (x - 1, y, 'S')]))
    elif dir == 'S' and x < SIZE - 1:
        pair = tuple(sorted([(x, y, 'S'), (x + 1, y, 'N')]))
    elif dir == 'E' and y < SIZE - 1:
        pair = tuple(sorted([(x, y, 'E'), (x, y + 1, 'W')]))
    elif dir == 'W' and y > 0:
        pair = tuple(sorted([(x, y, 'W'), (x, y - 1, 'E')]))
    else:
        pair = ((x, y, dir),)
    unique_walls.add(pair[0])  # Adiciona só uma das duas

# ---- COPIE ESTE BLOCO PARA O VISUALIZADOR ----
print("WALL_LIST = [")
for w in sorted(unique_walls):
    print(f"    {w},")
print("]")
