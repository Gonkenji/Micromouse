import pygame
from collections import deque

# ---- DIREÇÕES E CONSTANTES ----
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
DIRS = [NORTH, EAST, SOUTH, WEST]
DIR_OFFSETS = {
    NORTH: (-1, 0),
    EAST:  (0, 1),
    SOUTH: (1, 0),
    WEST:  (0, -1)
}
OPPOSITE = {NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}
SIZE = 16
CELL_SIZE = 30
WALL_WIDTH = 2
MARGIN = 20
WINDOW_SIZE = SIZE * CELL_SIZE + 2 * MARGIN

# ---- CLASSE DA CÉLULA ----
class Cell:
    def __init__(self):
        self.walls = 0b0000  # 4 bits: NESW
        self.visited = False
        self.distance = 255

    def set_wall(self, direction):
        self.walls |= (1 << direction)

    def has_wall(self, direction):
        return bool(self.walls & (1 << direction))

# ---- MAPA DO LABIRINTO ----
maze = [[Cell() for _ in range(SIZE)] for _ in range(SIZE)]

def add_wall(x, y, direction):
    maze[x][y].set_wall(direction)
    dx, dy = DIR_OFFSETS[direction]
    nx, ny = x + dx, y + dy
    if 0 <= nx < SIZE and 0 <= ny < SIZE:
        maze[nx][ny].set_wall(OPPOSITE[direction])

def flood_fill(goal_x, goal_y):
    for row in maze:
        for cell in row:
            cell.distance = 255
            cell.visited = False

    queue = deque()
    maze[goal_x][goal_y].distance = 0
    queue.append((goal_x, goal_y))

    while queue:
        x, y = queue.popleft()
        maze[x][y].visited = True
        for direction in DIRS:
            if maze[x][y].has_wall(direction):
                continue
            dx, dy = DIR_OFFSETS[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                new_dist = maze[x][y].distance + 1
                if maze[nx][ny].distance > new_dist:
                    maze[nx][ny].distance = new_dist
                    queue.append((nx, ny))

# ---- PYGAME: VISUALIZAÇÃO ----
def draw_maze(screen, font):
    for x in range(SIZE):
        for y in range(SIZE):
            cell = maze[x][y]
            screen_x = MARGIN + y * CELL_SIZE
            screen_y = MARGIN + x * CELL_SIZE

            # Célula preenchida se visitada
            if cell.visited:
                pygame.draw.rect(screen, (200, 200, 255), (screen_x, screen_y, CELL_SIZE, CELL_SIZE))

            # Desenha as paredes
            if cell.has_wall(NORTH):
                pygame.draw.line(screen, (0,0,0), (screen_x, screen_y), (screen_x + CELL_SIZE, screen_y), WALL_WIDTH)
            if cell.has_wall(EAST):
                pygame.draw.line(screen, (0,0,0), (screen_x + CELL_SIZE, screen_y), (screen_x + CELL_SIZE, screen_y + CELL_SIZE), WALL_WIDTH)
            if cell.has_wall(SOUTH):
                pygame.draw.line(screen, (0,0,0), (screen_x, screen_y + CELL_SIZE), (screen_x + CELL_SIZE, screen_y + CELL_SIZE), WALL_WIDTH)
            if cell.has_wall(WEST):
                pygame.draw.line(screen, (0,0,0), (screen_x, screen_y), (screen_x, screen_y + CELL_SIZE), WALL_WIDTH)

            # Mostra a distância
            if cell.distance != 255:
                text = font.render(str(cell.distance), True, (50, 50, 50))
                screen.blit(text, (screen_x + 5, screen_y + 5))

# ---- EXEMPLO: TESTE DE PAREDES ----
# Adiciona algumas paredes manualmente
add_wall(0, 0, EAST)
add_wall(0, 1, SOUTH)
add_wall(1, 1, WEST)
add_wall(1, 0, SOUTH)
add_wall(2, 0, EAST)

# Calcula a distância até o centro
flood_fill(7, 7)

# ---- LOOP PRINCIPAL DO PYGAME ----
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Micromouse Maze Viewer")
font = pygame.font.SysFont(None, 18)
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))
    draw_maze(screen, font)
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
