import pygame
import time
import math

N_LINHAS    = 16
TAM_CELULA  = 50
LARG_PAREDE = 2
MARGEM      = 20
LARG_JANELA = N_LINHAS * TAM_CELULA + 2 * MARGEM
ALT_JANELA  = LARG_JANELA

ACELERACAO   = 200.0   # px/s²
VEL_MAXIMA   = 200.0   # px/s
ATRITO       = 0.8    # percentual de redução por segundo

VELOCIDADE_ANGULAR = 90.0 # graus/s²
VEL_ANGULAR_MAXIMA = 180.0 # graus/s
ATRITO_ANGULAR     = 0.8   # Mais forte para parar giros rapidamente

FPS          = 60

pygame.init()
janela = pygame.display.set_mode((LARG_JANELA, ALT_JANELA))
pygame.display.set_caption("Micromouse")
relogio = pygame.time.Clock()

class Robo:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.angulo = 0
        self.v_angular = 0.0

    def mover(self):
        # --- Atualização Angular ---
        self.v_angular *= (1 - ATRITO_ANGULAR * dt)
        self.angulo += self.v_angular * dt
        self.angulo %= 360 # Mantém o ângulo entre 0 e 360

        # --- Atualização Linear ---

        # Atualiza velocidade com aceleração
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Calcula o vetor velocidade atual
        vel = pygame.math.Vector2(self.vx, self.vy)

        # Calcula o vetor de direção do ângulo atual
        direcao = pygame.math.Vector2(
            math.cos(math.radians(self.angulo)),
            math.sin(math.radians(self.angulo))
        )

        # Projeta a velocidade na direção do ângulo
        vel_proj = direcao * vel.dot(direcao)

        # Aplica atrito apenas na direção do movimento
        vel_proj *= (1 - ATRITO * dt)

        # Atualiza as velocidades filtradas (apenas na direção do ângulo)
        self.vx = vel_proj.x
        self.vy = vel_proj.y


        self.x += self.vx * dt
        self.y += self.vy * dt

        self.ax = self.ay = 0.0
        self.a_angular = 0.0

    def desenhar(self, superficie):
        # Corpo (quadrado vermelho)
        met = TAM_CELULA / 2

        # Cria uma superfície temporária para desenhar o robô não rotacionado
        robo_surf = pygame.Surface((met, met), pygame.SRCALPHA) # SRCALPHA para fundo transparente
        robo_surf.fill((0,0,0,0)) # Preenche com transparente
        pygame.draw.rect(robo_surf, (255, 255, 255), (0, 0, met, met))

        # Seta direcional (azul)
        tamanho_seta = TAM_CELULA // 4
        centro_x, centro_y = met / 2, met / 2 # Centro da superfície temporária
        # Pontos da seta apontando para cima (Norte = 0 graus)
        pontos_seta = [
            (centro_x - tamanho_seta, centro_y + tamanho_seta/2),
            (centro_x - tamanho_seta, centro_y - tamanho_seta/2), # Ponta
            (centro_x + tamanho_seta, centro_y)  # Base direita
        ]
        pygame.draw.polygon(robo_surf, (0, 0, 255), pontos_seta)

        # Rotaciona a superfície do robô
        # Pygame rotaciona anti-horário, então usamos o ângulo negativo
        # Ajuste de 90 graus porque nossa seta aponta para cima (N=0), mas 0 graus na matemática é para direita (E)
        # angulo_pygame = -(self.angulo - 90)
        angulo_pygame = -self.angulo # Se 0 graus for Norte, só precisa negar

        robo_rot_surf = pygame.transform.rotate(robo_surf, angulo_pygame)

        # Obtém o retângulo da superfície rotacionada e centraliza na posição do robô
        robo_rot_rect = robo_rot_surf.get_rect(center=(self.x, self.y))

        # Desenha (blit) a superfície rotacionada na tela principal
        superficie.blit(robo_rot_surf, robo_rot_rect)

robo = Robo()

running = True
while running:

    dt = relogio.tick(FPS) / 1000.0

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        robo.ax = ACELERACAO * math.cos(math.radians(robo.angulo))
        robo.ay = ACELERACAO * math.sin(math.radians(robo.angulo))

    elif keys[pygame.K_DOWN]:
        robo.ax = -ACELERACAO * math.cos(math.radians(robo.angulo))
        robo.ay = -ACELERACAO * math.sin(math.radians(robo.angulo))

    elif keys[pygame.K_LEFT]:
        robo.v_angular = -VELOCIDADE_ANGULAR

    elif keys[pygame.K_RIGHT]:
        robo.v_angular = VELOCIDADE_ANGULAR

    janela.fill((255, 255, 255))

    robo.mover()
    robo.desenhar(janela)
    pygame.display.flip()


pygame.quit()
