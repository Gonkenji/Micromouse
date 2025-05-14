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

VEL_ANGULAR_MAXIMA = 180.0 # graus/s
ATRITO_ANGULAR     = 0.8   # Mais forte para parar giros rapidamente

#azul
kpa = 250
kia = 0
kda = 20

kpang = 300
kiang = 0
kdang = 0

kpaa = 0
kiaa = 0
kdaa = 0

#verde
kpa2 = 200
kia2 = 0
kda2 = 20

kpang2 = 300
kiang2 = 0
kdang2 = 0

kpaa2 = 0
kiaa2 = 0
kdaa2 = 0

erroi = [0,0,0]
errod = [0,0,0]
erroant = [0,0,0]

dt = 1

FPS          = 60

pygame.init()
janela = pygame.display.set_mode((LARG_JANELA, ALT_JANELA))
pygame.display.set_caption("Micromouse")
relogio = pygame.time.Clock()

class Robo:
    def __init__(self, kpa, kpang, kia, kiang, kda, kdang, kpaa, kiaa, kdaa):
        self.x = TAM_CELULA
        self.y = TAM_CELULA
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.angulo = 0
        self.v_angular = 0.0
        self.kpa = kpa
        self.kpang = kpang
        self.kia = kia
        self.kiang = kiang
        self.kda = kda
        self.kdang = kdang
        self.kpaa = kpaa
        self.kiaa = kiaa
        self.kdaa = kdaa
        self.erroi = [0,0,0]
        self.errod = [0,0,0]
        self.erroant = [0,0,0]

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

    def controle(self, obj):
        errox = objetivo[obj][0] - self.x
        erroy = objetivo[obj][1] - self.y
        erroang = math.atan2(erroy, errox) - math.radians(self.angulo)

        erroang = (erroang + math.pi) % (2 * math.pi) - math.pi

        dist = math.hypot(errox, erroy)

        # 3. Normaliza o vetor direção
        if dist != 0:
            errox /= dist
            erroy /= dist

        self.erroi[0] += errox * dt
        self.erroi[1] += erroy * dt
        self.erroi[2] += erroang * dt

        self.errod[0] = (errox - self.erroant[0])/ dt
        self.errod[1] = (erroy - self.erroant[1])/ dt
        self.errod[2] = (erroang - self.erroant[2])/ dt   

        if abs(erroang - self.erroant[2])> 2:
            self.errod[2] = 0

        xproporcional = self.kpa * errox - self.kpaa * abs(erroang)
        xderivativo = self.kda * self.errod[0] - self.kdaa * abs(erroang)
        xintegral = self.kia * self.erroi[0] - self.kiaa * abs(erroang)

        yproporcional = self.kpa * erroy - self.kpaa * abs(erroang)
        yderivativo = self.kda * self.errod[1] - self.kdaa * abs(erroang)
        yintegral = self.kia * self.erroi[1] - self.kiaa * abs(erroang)

    
        if errox > 0:
            self.ax = abs(math.cos(math.radians(self.angulo)) * (xproporcional + xintegral + xderivativo))
            
        elif errox < 0:
            self.ax = -math.cos(math.radians(self.angulo)) * (xproporcional + xintegral + xderivativo)

        else:
            self.ax = 0

        if erroy > 0:
            self.ay = math.sin(math.radians(self.angulo)) * (yproporcional + yintegral + yderivativo)

        elif erroy < 0:
            self.ay = -math.sin(math.radians(self.angulo)) * (yproporcional + yintegral + yderivativo)

        else:
            self.ay = 0

        self.v_angular = erroang * self.kpang + self.kiang * self.erroi[2] + self.kdang * self.errod[2]

        

        if self.v_angular > VEL_ANGULAR_MAXIMA:
            self.v_angular = VEL_ANGULAR_MAXIMA
        elif self.v_angular < -VEL_ANGULAR_MAXIMA:
            self.v_angular = -VEL_ANGULAR_MAXIMA

        self.erroant[0] = errox
        self.erroant[1] = erroy
        self.erroant[2] = erroang

        if abs(self.x - objetivo[obj][0]) < 10 and abs(self.y - objetivo[obj][1]) < 10 and obj < len(objetivo):
            for i in range(3):
                self.erroi[i] = 0
                self.errod[i] = 0
                self.erroant[i] = 0
            obj += 1
        
        if obj == len(objetivo):
            obj = 0 
            
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



robo = Robo(kpa, kpang, kia, kiang, kda, kdang, kpaa, kiaa, kdaa)
robo2 = Robo(kpa2, kpang2, kia2, kiang2, kda2, kdang2, kpaa2, kiaa2, kdaa2)

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
        robo.a_angular = -VEL_ANGULAR_MAXIMA

    elif keys[pygame.K_RIGHT]:
        robo.a_angular = VEL_ANGULAR_MAXIMA

    obj = robo.controle(obj)
    obj2 = robo2.controle(obj2)

    janela.fill((255, 255, 255))

    robo.mover()
    robo.desenhar(janela, (0, 0, 255))
    robo2.mover()
    robo2.desenhar(janela, (0, 255, 0))

    pygame.display.flip()


pygame.quit()
