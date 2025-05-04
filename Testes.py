import pygame

# --- COLE AQUI SUA LISTA GERADA ---
WALL_LIST = [
    (8, 8, 'N'),
    (8, 8, 'S'),
    (8, 5, 'N'),
    (5, 5, 'W'),
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

# --- PLAYER ---
mouse_pos = [0, 0]  # Posição inicial (linha, coluna)
direcao = 'N'  # Direção inicial


# --- FUNÇÃO DE DESENHO ---
def draw_maze():
    screen.fill((255, 255, 255))

    for (x, y, dir) in WALL_LIST:
        screen_x = MARGIN + y * CELL_SIZE
        screen_y = MARGIN + x * CELL_SIZE
        line = DIR_LINES[dir](screen_x, screen_y)
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], WALL_WIDTH)
    
        # Desenhar o mouse
    # Centro da célula
    center_x = MARGIN + mouse_pos[1] * CELL_SIZE + CELL_SIZE // 2
    center_y = MARGIN + mouse_pos[0] * CELL_SIZE + CELL_SIZE // 2

    rect_size = CELL_SIZE // 2
    rect_offset = rect_size // 2

    # Desenhar o corpo do mouse (quadrado vermelho centralizado)
    pygame.draw.rect(screen, (255, 0, 0), (center_x - rect_offset, center_y - rect_offset, rect_size, rect_size))

    # Desenhar a direção do mouse (seta azul)
    arrow_size = CELL_SIZE // 4
    if direcao == 'N':
        pygame.draw.polygon(screen, (0, 0, 255), [
            (center_x, center_y - rect_offset),  # ponta
            (center_x - arrow_size // 2, center_y - rect_offset - arrow_size),
            (center_x + arrow_size // 2, center_y - rect_offset - arrow_size)
        ])
    elif direcao == 'S':
        pygame.draw.polygon(screen, (0, 0, 255), [
            (center_x, center_y + rect_offset),
            (center_x - arrow_size // 2, center_y + rect_offset + arrow_size),
            (center_x + arrow_size // 2, center_y + rect_offset + arrow_size)
        ])
    elif direcao == 'E':
        pygame.draw.polygon(screen, (0, 0, 255), [
            (center_x + rect_offset, center_y),
            (center_x + rect_offset + arrow_size, center_y - arrow_size // 2),
            (center_x + rect_offset + arrow_size, center_y + arrow_size // 2)
        ])
    elif direcao == 'W':
        pygame.draw.polygon(screen, (0, 0, 255), [
            (center_x - rect_offset, center_y),
            (center_x - rect_offset - arrow_size, center_y - arrow_size // 2),
            (center_x - rect_offset - arrow_size, center_y + arrow_size // 2)
        ])




def has_wall(x, y, dir):
    return (x, y, dir) in WALL_LIST


# --- LOOP PRINCIPAL ---
running = True
while running:
    draw_maze()
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
    x, y = mouse_pos

    if keys[pygame.K_UP] and not has_wall(x, y, 'N') and not has_wall(x - 1, y, 'S'):
        mouse_pos[0] -= 1
        direcao = 'N'

    elif keys[pygame.K_DOWN] and not has_wall(x, y, 'S') and not has_wall(x + 1, y, 'N'):
        mouse_pos[0] += 1
        direcao = 'S'

    elif keys[pygame.K_LEFT] and not has_wall(x, y, 'W') and not has_wall(x, y - 1, 'E'):
        mouse_pos[1] -= 1
        direcao = 'W'

    elif keys[pygame.K_RIGHT] and not has_wall(x, y, 'E') and not has_wall(x, y + 1, 'W'):
        mouse_pos[1] += 1
        direcao = 'E'


pygame.quit()
