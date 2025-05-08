import pygame
import time
import math
import random

objetivo = [
    (150, 50),
    (300, 180),
    (400, 300),
    (500, 450),
    (630, 630),   # próximo de (700, 700)
    (700, 700),
    (600, 800),
    (450, 800),
    (300, 800),
    (180, 700),
    (100, 600),
    (80, 450),
    (85, 250),
    (95, 120)  # fecha o caminho
]


obj = 0
obj2 = 0
objr = 0

N_LINHAS    = 20
TAM_CELULA  = 50
LARG_PAREDE = 2
MARGEM      = 20
LARG_JANELA = 1000
ALT_JANELA  = 1000

ACELERACAO   = 200.0   # px/s²
VEL_MAXIMA   = 200.0   # px/s
ATRITO       = 0.8    # percentual de redução por segundo

ACELERACAO_ANGULAR = 180.0 # graus/s²
VEL_ANGULAR_MAXIMA = 180.0 # graus/s
ATRITO_ANGULAR     = 0.8   # Mais forte para parar giros rapidamente

#azul
kpa = 60
kda = 25

kpang = 360
kdang = 180

#verde
kpa2 = 60
kda2 = 25

kpang2 = 180
kdang2 = 360

errod = [0,0,0]
erroant = [0,0,0]

dt = 1

FPS          = 60

pygame.init()
janela = pygame.display.set_mode((LARG_JANELA, ALT_JANELA))
pygame.display.set_caption("Micromouse")
relogio = pygame.time.Clock()

class Robo:
    def __init__(self, kpa, kpang, kda, kdang):
        self.x = TAM_CELULA
        self.y = TAM_CELULA
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.angulo = 0
        self.v_angular = 0.0
        self.a_angular = 0.0
        self.kpa = kpa
        self.kpang = kpang
        self.kda = kda
        self.kdang = kdang
        self.errod = [0,0,0]
        self.erroant = [0,0,0]

    def mover(self):
        # --- Atualização Angular ---
        self.v_angular += self.a_angular * dt
        self.v_angular *= (1 - ATRITO_ANGULAR * dt)
        self.angulo += self.v_angular * dt
        self.angulo %= 360 # Mantém o ângulo entre 0 e 360

        if self.v_angular > VEL_ANGULAR_MAXIMA:
            self.v_angular = VEL_ANGULAR_MAXIMA

        elif self.v_angular < -VEL_ANGULAR_MAXIMA:
            self.v_angular = -VEL_ANGULAR_MAXIMA

        # --- Atualização Linear ---

        self.vx += self.ax * dt
        self.vy += self.ay * dt

        self.vx *= (1 - ATRITO * dt)
        self.vy *= (1 - ATRITO * dt)

        if self.vx > VEL_MAXIMA:
            self.vx = VEL_MAXIMA
        elif self.vx < -VEL_MAXIMA:
            self.vx = -VEL_MAXIMA

        if self.vy > VEL_MAXIMA:
            self.vy = VEL_MAXIMA   
        elif self.vy < -VEL_MAXIMA:
            self.vy = -VEL_MAXIMA

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.ax = self.ay = 0.0
        self.a_angular = 0.0

    def controle(self, obj):

        errox = []
        erroy = []
        erroang = []

        for i in range(3):
            if obj == len(objetivo) - i:
                obj = -i
            errox.append(objetivo[obj+i][0] - self.x)
            erroy.append(objetivo[obj+i][1] - self.y)
            erroang.append(math.atan2(erroy[i], errox[i]) - math.radians(self.angulo))

        while abs(erroang[0] - erroang[1] - erroang[2]) < 0.01:
            obj += 1

            for i in range(3):
                if obj == len(objetivo) - i:
                    obj = -i
                errox.append(objetivo[obj][0] - self.x)
                erroy.append(objetivo[obj][1] - self.y)
                erroang.append(math.atan2(erroy[i], errox[i]) - math.radians(self.angulo))

        dist = math.hypot(errox[0], erroy[0])

        # 3. Normaliza o vetor direção
        if dist != 0:
            errox[0] /= dist
            erroy[0] /= dist

        self.errod[0] = (errox[0] - self.erroant[0])/ dt
        self.errod[1] = (erroy[0] - self.erroant[1])/ dt
        self.errod[2] = (erroang[0] - self.erroant[2])/ dt   

        if abs(erroang[0] - self.erroant[2])> 2:
            self.errod[2] = 0


        xproporcional = self.kpa * errox[0]
        xderivativo = self.kda * self.errod[0]

        yproporcional = self.kpa * erroy[0]
        yderivativo = self.kda * self.errod[1]

    
        if errox[0] > 0:
            self.ax = abs(math.cos(math.radians(self.angulo)) * (xproporcional + xderivativo))
            

        elif errox[0] < 0:
            self.ax = -math.cos(math.radians(self.angulo)) * (xproporcional + xderivativo)

        else:
            self.ax = 0

        if erroy[0] > 0:
            self.ay = math.sin(math.radians(self.angulo)) * (yproporcional + yderivativo)

        elif erroy[0] < 0:
            self.ay = -math.sin(math.radians(self.angulo)) * (yproporcional + yderivativo)

        else:
            self.ay = 0

        if erroang[0] >= math.pi:
            erroang[0] -= 2 * math.pi
        elif erroang[0] < -math.pi:
            erroang[0] += 2 * math.pi

        self.a_angular = erroang[0] * self.kpang + self.kdang * self.errod[2]

        self.erroant[0] = errox[0]
        self.erroant[1] = erroy[0]
        self.erroant[2] = erroang[0]

        if abs(self.x - objetivo[obj][0]) < 10 and abs(self.y - objetivo[obj][1]) < 10 and obj < len(objetivo):
            for i in range(3):
                self.errod[i] = 0
                self.erroant[i] = 0
            obj += 1
        
        return obj
        
    def desenhar(self, superficie, cor):

        for i in range(len(objetivo)):
            pygame.draw.circle(superficie, (255, 0, 0), (objetivo[i][0], objetivo[i][1]), 5)

        # Corpo (quadrado vermelho)
        met = TAM_CELULA / 2

        # Cria uma superfície temporária para desenhar o robô não rotacionado
        robo_surf = pygame.Surface((met, met), pygame.SRCALPHA) # SRCALPHA para fundo transparente
        robo_surf.fill((0,0,0,0)) # Preenche com transparente

        # Seta direcional (azul)
        tamanho_seta = TAM_CELULA // 4
        centro_x, centro_y = met / 2, met / 2 # Centro da superfície temporária
        # Pontos da seta apontando para cima (Norte = 0 graus)
        pontos_seta = [
            (centro_x - tamanho_seta, centro_y + tamanho_seta/2),
            (centro_x - tamanho_seta, centro_y - tamanho_seta/2), # Ponta
            (centro_x + tamanho_seta, centro_y)  # Base direita
        ]
        pygame.draw.polygon(robo_surf, cor, pontos_seta)

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



robo = Robo(kpa, kpang, kda, kdang)
robo2 = Robo(kpa2, kpang2, kda2, kdang2)

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
        robo.a_angular = -ACELERACAO_ANGULAR

    elif keys[pygame.K_RIGHT]:
        robo.a_angular = ACELERACAO_ANGULAR

    obj = robo.controle(obj)
    obj2 = robo2.controle(obj2)

    janela.fill((255, 255, 255))

    robo.mover()
    robo.desenhar(janela, (0, 0, 255))
    robo2.mover()
    robo2.desenhar(janela, (0, 255, 0))

    pygame.display.flip()


pygame.quit()