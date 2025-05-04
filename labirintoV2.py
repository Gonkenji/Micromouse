import pygame

# --- COLE AQUI SUA LISTA GERADA ---
WALL_LIST = [
    (7, 8, 'N'),
    (8, 8, 'S'),
    (8, 8, 'W'),
]

# --- CONSTANTES ---
SIZE = 16
CELL_SIZE = 30
WALL_WIDTH = 2
MARGIN = 20
WINDOW_SIZE = SIZE * CELL_SIZE + 2 * MARGIN

# --- DIREÇÕES ---
DIRS = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
DIR_LINES = {
    'N': lambda x, y: [(x, y), (x + CELL_SIZE, y)],
    'S': lambda x, y: [(x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE)],
    'E': lambda x, y: [(x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE)],
    'W': lambda x, y: [(x, y), (x, y + CELL_SIZE)],
}

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Labirinto do Micromouse")
clock = pygame.time.Clock()

# --- FUNÇÃO DE DESENHO ---
def draw_maze():
    screen.fill((255, 255, 255))

    for (x, y, dir) in WALL_LIST:
        screen_x = MARGIN + y * CELL_SIZE
        screen_y = MARGIN + x * CELL_SIZE
        line = DIR_LINES[dir](screen_x, screen_y)
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], WALL_WIDTH)

# --- LOOP PRINCIPAL ---
running = True
while running:
    draw_maze()
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
