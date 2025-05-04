import pygame
import time

# --- LISTA DE PAREDES GERADA ---
PAREDES = [
    (8, 8, 'N'),
    (8, 8, 'S'),
    (8, 5, 'N'),
    (5, 5, 'W'),
]

# --- CONSTANTES ---
N_LINHAS    = 16
TAM_CELULA  = 30
LARG_PAREDE = 2
MARGEM      = 20
LARG_JANELA = N_LINHAS * TAM_CELULA + 2 * MARGEM
ALT_JANELA  = LARG_JANELA

# Física
ACELERACAO   = 200.0   # px/s²
VEL_MAXIMA   = 200.0   # px/s
ATRITO       = 0.8     # percentual de redução por segundo
FPS          = 60

# Pygame
pygame.init()
janela = pygame.display.set_mode((LARG_JANELA, ALT_JANELA))
pygame.display.set_caption("Micromouse")
relogio = pygame.time.Clock()

# Função de colisão

def tem_parede(lin, col, direcao):
    return (lin, col, direcao) in PAREDES

# Classe do robô
class Robo:
    def __init__(self, celula_inicial=(0, 0)):
        lin, col = celula_inicial
        self.x = MARGEM + col * TAM_CELULA + TAM_CELULA / 2
        self.y = MARGEM + lin * TAM_CELULA + TAM_CELULA / 2
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.direcao = 'N'

    def processar_entrada(self, teclas):
        self.ax = 0.0
        self.ay = 0.0
        lin = int((self.y - MARGEM) // TAM_CELULA)
        col = int((self.x - MARGEM) // TAM_CELULA)

        if teclas[pygame.K_LEFT]:
            print(f"Sensor lateral: W={tem_parede(lin, col, 'W')}, E={tem_parede(lin, col, 'E')}")
            self.ax = -ACELERACAO
            self.direcao = 'W'
        if teclas[pygame.K_RIGHT]:
            print(f"Sensor lateral: E={tem_parede(lin, col, 'E')}, W={tem_parede(lin, col, 'W')}")
            self.ax = ACELERACAO
            self.direcao = 'E'
        if teclas[pygame.K_UP]:
            print(f"Sensor vertical: N={tem_parede(lin, col, 'N')}, S={tem_parede(lin, col, 'S')}")
            self.ay = -ACELERACAO
            self.direcao = 'N'
        if teclas[pygame.K_DOWN]:
            print(f"Sensor vertical: S={tem_parede(lin, col, 'S')}, N={tem_parede(lin, col, 'N')}")
            self.ay = ACELERACAO
            self.direcao = 'S'

    def atualizar(self, dt):
        # Atualiza velocidade com aceleração
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        # Aplica atrito
        self.vx *= (1 - ATRITO * dt)
        self.vy *= (1 - ATRITO * dt)
        # Limita velocidade
        if abs(self.vx) > VEL_MAXIMA:
            self.vx = VEL_MAXIMA * (1 if self.vx > 0 else -1)
        if abs(self.vy) > VEL_MAXIMA:
            self.vy = VEL_MAXIMA * (1 if self.vy > 0 else -1)

        # Metade do tamanho do robô (distância do centro à borda)
        metade_robo = TAM_CELULA / 4.0

        # Célula atual
        lin = int((self.y - MARGEM) // TAM_CELULA)
        col = int((self.x - MARGEM) // TAM_CELULA)

        # --- Colisão e Movimento no Eixo X ---
        dx = self.vx * dt
        potencial_x = self.x + dx

        if dx > 0: # Movendo para Direita
            borda_direita_robo = potencial_x + metade_robo
            limite_parede_direita = MARGEM + (col + 1) * TAM_CELULA
            # Verifica se a borda direita ultrapassaria o limite E se existe parede
            if borda_direita_robo >= limite_parede_direita and (tem_parede(lin, col, 'E') or tem_parede(lin, col + 1, 'W')):
                self.vx = 0
                # Ajusta a posição para encostar na parede
                self.x = limite_parede_direita - metade_robo
            else:
                self.x = potencial_x # Move normalmente
        elif dx < 0: # Movendo para Esquerda
            borda_esquerda_robo = potencial_x - metade_robo
            limite_parede_esquerda = MARGEM + col * TAM_CELULA
            # Verifica se a borda esquerda ultrapassaria o limite W se existe parede
            if borda_esquerda_robo <= limite_parede_esquerda and (tem_parede(lin, col, 'W') or tem_parede(lin, col - 1, 'E')):
                self.vx = 0
                # Ajusta a posição para encostar na parede
                self.x = limite_parede_esquerda + metade_robo
            else:
                self.x = potencial_x # Move normalmente

        # --- Colisão e Movimento no Eixo Y ---
        dy = self.vy * dt
        potencial_y = self.y + dy

        if dy > 0: # Movendo para Baixo
            borda_baixo_robo = potencial_y + metade_robo
            limite_parede_baixo = MARGEM + (lin + 1) * TAM_CELULA
            if borda_baixo_robo >= limite_parede_baixo and (tem_parede(lin, col, 'S') or tem_parede(lin + 1, col, 'N')):
                self.vy = 0
                self.y = limite_parede_baixo - metade_robo
            else:
                self.y = potencial_y
        elif dy < 0: # Movendo para Cima
            borda_cima_robo = potencial_y - metade_robo
            limite_parede_cima = MARGEM + lin * TAM_CELULA
            if borda_cima_robo <= limite_parede_cima and (tem_parede(lin, col, 'N') or tem_parede(lin - 1, col, 'S')):
                self.vy = 0
                self.y = limite_parede_cima + metade_robo
            else:
                self.y = potencial_y

    def desenhar(self, superficie):
        # Corpo (quadrado vermelho)
        met = TAM_CELULA / 2
        pygame.draw.rect(
            superficie,
            (255, 0, 0),
            (self.x - met/2, self.y - met/2, met, met)
        )
        # Seta direcional (azul)
        tamanho_seta = TAM_CELULA // 4
        off = met / 2
        if self.direcao == 'N':
            pontos = [(self.x, self.y-off),
                      (self.x-tamanho_seta/2, self.y-off-tamanho_seta),
                      (self.x+tamanho_seta/2, self.y-off-tamanho_seta)]
        elif self.direcao == 'S':
            pontos = [(self.x, self.y+off),
                      (self.x-tamanho_seta/2, self.y+off+tamanho_seta),
                      (self.x+tamanho_seta/2, self.y+off+tamanho_seta)]
        elif self.direcao == 'E':
            pontos = [(self.x+off, self.y),
                      (self.x+off+tamanho_seta, self.y-tamanho_seta/2),
                      (self.x+off+tamanho_seta, self.y+tamanho_seta/2)]
        else:  # W
            pontos = [(self.x-off, self.y),
                      (self.x-off-tamanho_seta, self.y-tamanho_seta/2),
                      (self.x-off-tamanho_seta, self.y+tamanho_seta/2)]
        pygame.draw.polygon(superficie, (0, 0, 255), pontos)

# Instancia o robô
robo = Robo(celula_inicial=(0, 0))

# Função para desenhar o labirinto

def desenhar_labirinto(superficie):
    superficie.fill((255, 255, 255))
    for lin, col, d in PAREDES:
        sx = MARGEM + col * TAM_CELULA
        sy = MARGEM + lin * TAM_CELULA
        if d == 'N':
            pygame.draw.line(superficie, (0, 0, 0), (sx, sy), (sx+TAM_CELULA, sy), LARG_PAREDE)
        elif d == 'S':
            pygame.draw.line(superficie, (0, 0, 0), (sx, sy+TAM_CELULA), (sx+TAM_CELULA, sy+TAM_CELULA), LARG_PAREDE)
        elif d == 'E':
            pygame.draw.line(superficie, (0, 0, 0), (sx+TAM_CELULA, sy), (sx+TAM_CELULA, sy+TAM_CELULA), LARG_PAREDE)
        else:  # W
            pygame.draw.line(superficie, (0, 0, 0), (sx, sy), (sx, sy+TAM_CELULA), LARG_PAREDE)

# Loop principal
executando = True
while executando:
    dt = relogio.tick(FPS) / 1000.0
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    teclas = pygame.key.get_pressed()
    robo.processar_entrada(teclas)
    robo.atualizar(dt)

    desenhar_labirinto(janela)
    robo.desenhar(janela)
    pygame.display.flip()

pygame.quit()
