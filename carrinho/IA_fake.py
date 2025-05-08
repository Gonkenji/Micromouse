import pygame
import time
import math
import random

objetivo = [(500,500), (100,100), (100,500)]
obj = 0

objr = [0 for _ in range(10)]

N_LINHAS    = 16
TAM_CELULA  = 50
LARG_PAREDE = 2
MARGEM      = 20
LARG_JANELA = N_LINHAS * TAM_CELULA + 2 * MARGEM
ALT_JANELA  = LARG_JANELA

ACELERACAO   = 200.0   # px/s²
VEL_MAXIMA   = 200.0   # px/s
ATRITO       = 0.8    # percentual de redução por segundo

ACELERACAO_ANGULAR = 180.0 # graus/s²
VEL_ANGULAR_MAXIMA = 180.0 # graus/s
ATRITO_ANGULAR     = 0.8   # Mais forte para parar giros rapidamente


kpa = 50
kia = 0
kda = 2

kpang = 30
kiang = 5
kdang = 2

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
    def __init__(self, kpa, kpang, kia, kiang, kda, kdang, cor):
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
        self.kia = kia
        self.kiang = kiang
        self.kda = kda
        self.kdang = kdang
        self.cor = cor

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
        errox = objetivo[obj][0] - self.x
        erroy = objetivo[obj][1] - self.y
        erroang = math.atan2(erroy, errox) - math.radians(self.angulo)

        dist = math.hypot(errox, erroy)

        # 3. Normaliza o vetor direção
        if dist != 0:
            errox /= dist
            erroy /= dist


        erroi[0] += errox * dt
        erroi[1] += erroy * dt
        erroi[2] += erroang * dt

        errod[0] = (errox - erroant[0])/ dt
        errod[1] = (erroy - erroant[1])/ dt
        errod[2] = (erroang - erroant[2])/ dt

        #print(errod[0])

        if errox > 0:
            self.ax = math.cos(math.radians(self.angulo)) * (errox * self.kpa + self.kia * erroi[0] + self.kda * errod[0])
            

        elif errox < 0:
            self.ax = -math.cos(math.radians(self.angulo)) * (errox * self.kpa + self.kia * erroi[0] + self.kda * errod[0])

        else:
            self.ax = 0

        if erroy > 0:
            self.ay = math.sin(math.radians(self.angulo)) * (erroy * self.kpa + self.kia * erroi[1] + self.kda * errod[1])

        elif erroy < 0:
            self.ay = -math.sin(math.radians(self.angulo)) * (erroy * self.kpa + self.kia * erroi[1] + self.kda * errod[1])

        else:
            self.ay = 0

        if erroang > math.pi:
            erroang -= 2 * math.pi
        elif erroang < -math.pi:
            erroang += 2 * math.pi

        self.a_angular = erroang * self.kpang + self.kiang * erroi[2] + self.kdang * errod[2]

        if abs(self.x - objetivo[obj][0]) < 10 and abs(self.y - objetivo[obj][1]) < 10 and obj < len(objetivo):
            for i in range(3):
                erroi[i] = 0
                errod[i] = 0
                erroant[i] = 0
                

            obj += 1
        
        if obj == len(objetivo):
            obj = 0 
        return obj
        
    def desenhar(self, superficie):

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
        pygame.draw.polygon(robo_surf, self.cor, pontos_seta)

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



robo = Robo(kpa, kpang, kia, kiang, kda, kdang, (0, 0, 255))

robos = []

for i in range(10):
    robos.append(Robo(random.uniform(-100,100),random.randint(-180,180),random.uniform(-50,50),random.randint(-90,90),random.uniform(-50,50),random.randint(-90,90), (random.randint(0,255),random.randint(0,255),random.randint(0,255))))

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

    for n,r in enumerate(robos):
        objr[n] = r.controle(objr[n])

    janela.fill((255, 255, 255))

    robo.mover()
    robo.desenhar(janela)

    for i in robos:
        i.mover()
        i.desenhar(janela)

    pygame.display.flip()


pygame.quit()