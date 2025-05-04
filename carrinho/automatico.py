import pygame
import time
import math # Importa o módulo math

# --- LISTA DE PAREDES GERADA ---
PAREDES = [
    (0, 0, 'N'),
    (0, 0, 'W'),
    (0, 1, 'N'),
    (0, 2, 'N'),
    (0, 2, 'S'),
    (0, 3, 'N'),
    (0, 3, 'S'),
    (0, 4, 'N'),
    (0, 4, 'S'),
    (0, 5, 'N'),
    (0, 5, 'S'),
    (0, 6, 'E'),
    (0, 6, 'N'),
    (0, 7, 'N'),
    (0, 8, 'E'),
    (0, 8, 'N'),
    (0, 9, 'N'),
    (0, 9, 'S'),
    (0, 10, 'N'),
    (0, 11, 'E'),
    (0, 11, 'N'),
    (0, 12, 'N'),
    (0, 12, 'S'),
    (0, 13, 'N'),
    (0, 13, 'S'),
    (0, 14, 'N'),
    (0, 14, 'S'),
    (0, 15, 'E'),
    (0, 15, 'N'),
    (1, 0, 'E'),
    (1, 0, 'W'),
    (1, 1, 'S'),
    (1, 2, 'S'),
    (1, 3, 'E'),
    (1, 5, 'E'),
    (1, 6, 'S'),
    (1, 7, 'E'),
    (1, 7, 'S'),
    (1, 8, 'E'),
    (1, 10, 'E'),
    (1, 10, 'S'),
    (1, 11, 'S'),
    (1, 12, 'S'),
    (1, 13, 'S'),
    (1, 14, 'E'),
    (1, 15, 'E'),
    (2, 0, 'S'),
    (2, 0, 'W'),
    (2, 1, 'E'),
    (2, 2, 'E'),
    (2, 3, 'S'),
    (2, 4, 'E'),
    (2, 4, 'S'),
    (2, 5, 'S'),
    (2, 6, 'E'),
    (2, 7, 'S'),
    (2, 8, 'S'),
    (2, 9, 'E'),
    (2, 9, 'S'),
    (2, 11, 'S'),
    (2, 12, 'S'),
    (2, 13, 'S'),
    (2, 14, 'E'),
    (2, 14, 'S'),
    (2, 15, 'E'),
    (3, 0, 'W'),
    (3, 1, 'E'),
    (3, 1, 'S'),
    (3, 2, 'S'),
    (3, 4, 'S'),
    (3, 5, 'E'),
    (3, 6, 'S'),
    (3, 7, 'E'),
    (3, 8, 'E'),
    (3, 10, 'E'),
    (3, 10, 'S'),
    (3, 11, 'E'),
    (3, 14, 'E'),
    (3, 15, 'E'),
    (4, 0, 'E'),
    (4, 0, 'W'),
    (4, 2, 'S'),
    (4, 3, 'E'),
    (4, 3, 'S'),
    (4, 5, 'E'),
    (4, 5, 'S'),
    (4, 6, 'E'),
    (4, 7, 'E'),
    (4, 8, 'S'),
    (4, 9, 'E'),
    (4, 10, 'S'),
    (4, 11, 'S'),
    (4, 12, 'E'),
    (4, 12, 'S'),
    (4, 13, 'E'),
    (4, 14, 'S'),
    (4, 15, 'E'),
    (5, 0, 'S'),
    (5, 0, 'W'),
    (5, 1, 'E'),
    (5, 1, 'S'),
    (5, 3, 'E'),
    (5, 4, 'E'),
    (5, 6, 'E'),
    (5, 6, 'S'),
    (5, 7, 'S'),
    (5, 8, 'E'),
    (5, 9, 'S'),
    (5, 10, 'S'),
    (5, 11, 'S'),
    (5, 12, 'E'),
    (5, 13, 'S'),
    (5, 14, 'E'),
    (5, 15, 'E'),
    (6, 0, 'W'),
    (6, 2, 'E'),
    (6, 2, 'S'),
    (6, 3, 'E'),
    (6, 3, 'S'),
    (6, 4, 'S'),
    (6, 5, 'E'),
    (6, 7, 'S'),
    (6, 8, 'E'),
    (6, 8, 'S'),
    (6, 10, 'E'),
    (6, 12, 'E'),
    (6, 12, 'S'),
    (6, 14, 'E'),
    (6, 14, 'S'),
    (6, 15, 'E'),
    (7, 0, 'E'),
    (7, 0, 'W'),
    (7, 1, 'S'),
    (7, 2, 'E'),
    (7, 4, 'S'),
    (7, 5, 'E'),
    (7, 5, 'S'),
    (7, 6, 'S'),
    (7, 7, 'E'),
    (7, 9, 'E'),
    (7, 9, 'S'),
    (7, 10, 'E'),
    (7, 11, 'E'),
    (7, 12, 'S'),
    (7, 13, 'E'),
    (7, 14, 'S'),
    (7, 15, 'E'),
    (8, 0, 'S'),
    (8, 0, 'W'),
    (8, 1, 'E'),
    (8, 2, 'S'),
    (8, 3, 'E'),
    (8, 3, 'S'),
    (8, 4, 'E'),
    (8, 6, 'S'),
    (8, 7, 'E'),
    (8, 7, 'S'),
    (8, 8, 'S'),
    (8, 9, 'E'),
    (8, 9, 'S'),
    (8, 10, 'E'),
    (8, 11, 'S'),
    (8, 12, 'E'),
    (8, 13, 'S'),
    (8, 14, 'E'),
    (8, 15, 'E'),
    (9, 0, 'E'),
    (9, 0, 'W'),
    (9, 1, 'S'),
    (9, 2, 'S'),
    (9, 4, 'E'),
    (9, 4, 'S'),
    (9, 5, 'E'),
    (9, 7, 'S'),
    (9, 8, 'S'),
    (9, 9, 'E'),
    (9, 10, 'S'),
    (9, 11, 'S'),
    (9, 12, 'S'),
    (9, 13, 'S'),
    (9, 14, 'E'),
    (9, 14, 'S'),
    (9, 15, 'E'),
    (10, 0, 'E'),
    (10, 0, 'W'),
    (10, 2, 'S'),
    (10, 3, 'E'),
    (10, 3, 'S'),
    (10, 5, 'E'),
    (10, 5, 'S'),
    (10, 6, 'S'),
    (10, 7, 'S'),
    (10, 8, 'E'),
    (10, 9, 'S'),
    (10, 10, 'S'),
    (10, 11, 'S'),
    (10, 12, 'E'),
    (10, 13, 'S'),
    (10, 14, 'E'),
    (10, 15, 'E'),
    (11, 0, 'E'),
    (11, 0, 'W'),
    (11, 2, 'S'),
    (11, 3, 'E'),
    (11, 3, 'S'),
    (11, 4, 'S'),
    (11, 5, 'S'),
    (11, 6, 'S'),
    (11, 8, 'S'),
    (11, 9, 'S'),
    (11, 10, 'S'),
    (11, 11, 'E'),
    (11, 12, 'S'),
    (11, 13, 'E'),
    (11, 15, 'E'),
    (11, 15, 'S'),
    (12, 0, 'W'),
    (12, 1, 'E'),
    (12, 1, 'S'),
    (12, 3, 'E'),
    (12, 5, 'S'),
    (12, 6, 'E'),
    (12, 7, 'S'),
    (12, 8, 'E'),
    (12, 8, 'S'),
    (12, 10, 'E'),
    (12, 11, 'E'),
    (12, 11, 'S'),
    (12, 13, 'E'),
    (12, 13, 'S'),
    (12, 14, 'S'),
    (12, 15, 'E'),
    (13, 0, 'E'),
    (13, 0, 'S'),
    (13, 0, 'W'),
    (13, 2, 'E'),
    (13, 2, 'S'),
    (13, 3, 'S'),
    (13, 4, 'E'),
    (13, 4, 'S'),
    (13, 6, 'S'),
    (13, 7, 'S'),
    (13, 8, 'S'),
    (13, 9, 'E'),
    (13, 9, 'S'),
    (13, 10, 'S'),
    (13, 11, 'E'),
    (13, 12, 'E'),
    (13, 13, 'S'),
    (13, 14, 'E'),
    (13, 15, 'E'),
    (14, 0, 'W'),
    (14, 1, 'E'),
    (14, 1, 'S'),
    (14, 2, 'S'),
    (14, 3, 'S'),
    (14, 4, 'S'),
    (14, 5, 'S'),
    (14, 6, 'E'),
    (14, 6, 'S'),
    (14, 7, 'S'),
    (14, 8, 'E'),
    (14, 10, 'E'),
    (14, 10, 'S'),
    (14, 11, 'S'),
    (14, 12, 'E'),
    (14, 12, 'S'),
    (14, 14, 'E'),
    (14, 14, 'S'),
    (14, 15, 'E'),
    (15, 0, 'S'),
    (15, 0, 'W'),
    (15, 1, 'S'),
    (15, 2, 'S'),
    (15, 3, 'S'),
    (15, 4, 'S'),
    (15, 5, 'S'),
    (15, 6, 'S'),
    (15, 7, 'S'),
    (15, 8, 'S'),
    (15, 9, 'S'),
    (15, 10, 'S'),
    (15, 11, 'S'),
    (15, 12, 'S'),
    (15, 13, 'S'),
    (15, 14, 'S'),
    (15, 15, 'E'),
    (15, 15, 'S'),
]

# --- CONSTANTES ---
N_LINHAS    = 16
TAM_CELULA  = 30
LARG_PAREDE = 2
MARGEM      = 20
LARG_JANELA = N_LINHAS * TAM_CELULA + 2 * MARGEM
ALT_JANELA  = LARG_JANELA

# Física Linear
ACELERACAO   = 50.0   # px/s²
VEL_MAXIMA   = 200.0   # px/s
ATRITO       = 0.8     # percentual de redução por segundo

# Física Angular
ACELERACAO_ANGULAR = 90.0 # graus/s²
VEL_ANGULAR_MAXIMA = 180.0 # graus/s
ATRITO_ANGULAR     = 1.5   # Mais forte para parar giros rapidamente
FPS          = 60
# Pygame
pygame.init()
janela = pygame.display.set_mode((LARG_JANELA, ALT_JANELA))
pygame.display.set_caption("Micromouse")
relogio = pygame.time.Clock()

# Função de colisão

def tem_parede(lin, col, direcao):
    return (lin, col, direcao) in PAREDES


ESQUERDA = {'N':'W', 'W':'S', 'S':'E', 'E':'N'}
DIREITA = {'N':'E', 'E':'S', 'S':'W', 'W':'N'}

# --- CAMINHO A SEGUIR ---
# Lista de tuplas (linha, coluna)
CAMINHO_ALVO = [
    (0, 5),
    (5, 5),
    (5, 10),
    (10, 10),
    (10, 0),
]
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
        # self.direcao = 'E' # Substituído por ângulo
        self.angulo = 90.0 # 0=N, 90=E, 180=S, 270=W (Começa virado para direita)
        self.v_angular = 0.0
        self.a_angular = 0.0
        self.indice_caminho = 0 # Índice do ponto atual no CAMINHO_ALVO

    def obter_celula(self):
        lin = int((self.y - MARGEM) // TAM_CELULA)
        col = int((self.x - MARGEM) // TAM_CELULA)
        return lin, col

    def calcular_distancia_parede(self, sentido):
        lin, col = self.obter_celula()
        metade_robo = TAM_CELULA / 4.0
        # Verifica limites antes de chamar tem_parede para célula vizinha
        # Verifica parede na célula atual
        if sentido == 'N' and (tem_parede(lin, col, 'N') or (lin > 0 and tem_parede(lin - 1, col, 'S'))):
            dist_parede = MARGEM + lin * TAM_CELULA
            dist_borda_robo = self.y - metade_robo
            return max(0, dist_borda_robo - dist_parede)
        elif sentido == 'S' and (tem_parede(lin, col, 'S') or (lin + 1 < N_LINHAS and tem_parede(lin + 1, col, 'N'))):
            dist_parede = MARGEM + (lin + 1) * TAM_CELULA
            dist_borda_robo = self.y + metade_robo
            return max(0, dist_parede - dist_borda_robo)
        elif sentido == 'E' and (tem_parede(lin, col, 'E') or (col + 1 < N_LINHAS and tem_parede(lin, col + 1, 'W'))):
            dist_parede = MARGEM + (col + 1) * TAM_CELULA
            dist_borda_robo = self.x + metade_robo
            return max(0, dist_parede - dist_borda_robo)
        elif sentido == 'W' and (tem_parede(lin, col, 'W') or (col > 0 and tem_parede(lin, col - 1, 'E'))):
            dist_parede = MARGEM + col * TAM_CELULA
            dist_borda_robo = self.x - metade_robo
            return max(0, dist_borda_robo - dist_parede)

        # Conta células livres até a próxima parede
        celulas_ate_parede = 0
        atual_lin, atual_col = lin, col
        while True:
            if sentido == 'N': atual_lin -= 1
            elif sentido == 'S': atual_lin += 1
            elif sentido == 'E': atual_col += 1
            else: atual_col -= 1

            if not (0 <= atual_lin < N_LINHAS and 0 <= atual_col < N_LINHAS):
                break
            oposta = {'N':'S','S':'N','E':'W','W':'E'}[sentido]
            if tem_parede(atual_lin, atual_col, oposta):
                break
            celulas_ate_parede += 1

        # Calcula distância da borda do robô até a borda da célula atual
        if sentido == 'N': dist_na_celula = (self.y - metade_robo) - (MARGEM + lin * TAM_CELULA)
        elif sentido == 'S': dist_na_celula = (MARGEM + (lin + 1) * TAM_CELULA) - (self.y + metade_robo)
        elif sentido == 'E': dist_na_celula = (MARGEM + (col + 1) * TAM_CELULA) - (self.x + metade_robo)
        else: # W
            dist_na_celula = (self.x - metade_robo) - (MARGEM + col * TAM_CELULA)

        distancia_total = dist_na_celula + celulas_ate_parede * TAM_CELULA
        return max(0, distancia_total)

    def calcular_angulo_para_alvo(self, alvo_x, alvo_y):
        """Calcula o ângulo (0-360, 0=N) do robô para o ponto alvo."""
        delta_x = alvo_x - self.x
        delta_y = alvo_y - self.y # Y do Pygame cresce para baixo
        # Calcula o ângulo em radianos e converte para graus
        rad = math.atan2(delta_x, -delta_y) # atan2(x, -y) para 0=N
        graus = math.degrees(rad)
        return (graus + 360) % 360 # Normaliza para 0-360

    def move_robo(self):
        """Decide a próxima ação do robô com base nos sensores (seguir parede esquerda)."""
        # Reseta acelerações a cada decisão
        self.a_angular = 0.0
        aceleracao_frente = 0.0 # Aceleração linear desejada

        lin, col = self.obter_celula()

        # --- Lógica de Seguir Caminho ---
        if self.indice_caminho >= len(CAMINHO_ALVO):
            print("Fim do caminho alcançado!")
            self.ax = self.ay = 0.0 # Para o robô
            self.a_angular = 0.0
            return # Não faz mais nada

        # Pega a célula alvo atual
        alvo_lin, alvo_col = CAMINHO_ALVO[self.indice_caminho]
        # Calcula as coordenadas em pixel do centro da célula alvo
        alvo_x = MARGEM + alvo_col * TAM_CELULA + TAM_CELULA / 2
        alvo_y = MARGEM + alvo_lin * TAM_CELULA + TAM_CELULA / 2

        # Verifica se chegou perto do alvo atual
        dist_x = alvo_x - self.x
        dist_y = alvo_y - self.y
        dist_ao_quadrado = dist_x**2 + dist_y**2
        distancia_para_chegar = TAM_CELULA * 0.5 # Metade da célula

        if dist_ao_quadrado < (distancia_para_chegar**2):
            print(f"Chegou ao ponto {self.indice_caminho}: ({alvo_lin}, {alvo_col})")
            self.indice_caminho += 1
            # Se ainda houver caminho, recalcula alvo para o próximo ponto
            if self.indice_caminho < len(CAMINHO_ALVO):
                alvo_lin, alvo_col = CAMINHO_ALVO[self.indice_caminho]
                alvo_x = MARGEM + alvo_col * TAM_CELULA + TAM_CELULA / 2
                alvo_y = MARGEM + alvo_lin * TAM_CELULA + TAM_CELULA / 2
            else:
                print("Fim do caminho alcançado!")
                self.ax = self.ay = 0.0
                return # Sai da função se acabou o caminho

        # Determina direções cardeais relativas ao ângulo atual
        angulo_norm = self.angulo % 360
        if 315 <= angulo_norm < 360 or 0 <= angulo_norm < 45: frente = 'N'
        elif 45 <= angulo_norm < 135: frente = 'E'
        elif 135 <= angulo_norm < 225: frente = 'S'
        else: frente = 'W' # 225 <= angulo_norm < 315

        # Calcula o ângulo desejado para o alvo
        angulo_desejado = self.calcular_angulo_para_alvo(alvo_x, alvo_y)

        # Calcula a diferença de ângulo (considerando a volta 0/360)
        erro_angulo = angulo_desejado - self.angulo
        if erro_angulo > 180: erro_angulo -= 360
        if erro_angulo < -180: erro_angulo += 360

        # Controlador Proporcional (P) para a aceleração angular
        # Ajuste o ganho (Kp) conforme necessário
        kp_angular = 2.0
        self.a_angular = kp_angular * erro_angulo

        # Limita a aceleração angular para não ser excessiva
        max_a_angular_controlada = ACELERACAO_ANGULAR * 1.5
        if abs(self.a_angular) > max_a_angular_controlada:
            self.a_angular = max_a_angular_controlada * (1 if self.a_angular > 0 else -1)

        # Define aceleração para frente apenas se estiver razoavelmente alinhado
        angulo_tolerancia = 15.0 # Graus
        if abs(erro_angulo) < angulo_tolerancia:
            aceleracao_frente = ACELERACAO
        else:
            aceleracao_frente = ACELERACAO * 0.2 # Anda devagar se não alinhado

        # Define aceleração linear com base no ângulo atual e aceleração_frente
        rad_angle = math.radians(self.angulo)
        self.ax = aceleracao_frente * math.sin(rad_angle)
        self.ay = -aceleracao_frente * math.cos(rad_angle) # Negativo para Y do Pygame

    def atualizar(self, dt):
        # --- Atualização Angular ---
        self.v_angular += self.a_angular * dt
        # Atrito angular
        self.v_angular *= (1 - ATRITO_ANGULAR * dt)
        # Limita velocidade angular
        if abs(self.v_angular) > VEL_ANGULAR_MAXIMA:
             self.v_angular = VEL_ANGULAR_MAXIMA * (1 if self.v_angular > 0 else -1)
        # Atualiza ângulo
        self.angulo += self.v_angular * dt
        self.angulo %= 360 # Mantém o ângulo entre 0 e 360

        # --- Atualização Linear ---
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
            if borda_direita_robo >= limite_parede_direita and (tem_parede(lin, col, 'E') or (col + 1 < N_LINHAS and tem_parede(lin, col + 1, 'W'))):
                self.vx = 0
                # Ajusta a posição para encostar na parede
                self.x = limite_parede_direita - metade_robo
            else:
                self.x = potencial_x # Move normalmente
        elif dx < 0: # Movendo para Esquerda
            borda_esquerda_robo = potencial_x - metade_robo
            limite_parede_esquerda = MARGEM + col * TAM_CELULA
            # Verifica se a borda esquerda ultrapassaria o limite W se existe parede
            if borda_esquerda_robo <= limite_parede_esquerda and (tem_parede(lin, col, 'W') or (col > 0 and tem_parede(lin, col - 1, 'E'))):
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
            if borda_baixo_robo >= limite_parede_baixo and (tem_parede(lin, col, 'S') or (lin + 1 < N_LINHAS and tem_parede(lin + 1, col, 'N'))):
                self.vy = 0
                self.y = limite_parede_baixo - metade_robo
            else:
                self.y = potencial_y
        elif dy < 0: # Movendo para Cima
            borda_cima_robo = potencial_y - metade_robo
            limite_parede_cima = MARGEM + lin * TAM_CELULA
            if borda_cima_robo <= limite_parede_cima and (tem_parede(lin, col, 'N') or (lin > 0 and tem_parede(lin - 1, col, 'S'))):
                self.vy = 0
                self.y = limite_parede_cima + metade_robo
            else:
                self.y = potencial_y
    def desenhar(self, superficie):
        # Corpo (quadrado vermelho)
        met = TAM_CELULA / 2

        # Cria uma superfície temporária para desenhar o robô não rotacionado
        robo_surf = pygame.Surface((met, met), pygame.SRCALPHA) # SRCALPHA para fundo transparente
        robo_surf.fill((0,0,0,0)) # Preenche com transparente
        pygame.draw.rect(robo_surf, (255, 0, 0), (0, 0, met, met))

        # Seta direcional (azul)
        tamanho_seta = TAM_CELULA // 4
        centro_x, centro_y = met / 2, met / 2 # Centro da superfície temporária
        # Pontos da seta apontando para cima (Norte = 0 graus)
        pontos_seta = [
            (centro_x, centro_y - tamanho_seta * 0.7), # Ponta
            (centro_x - tamanho_seta / 2, centro_y + tamanho_seta * 0.3), # Base esquerda
            (centro_x + tamanho_seta / 2, centro_y + tamanho_seta * 0.3)  # Base direita
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

    robo.move_robo()
    robo.atualizar(dt)

    desenhar_labirinto(janela)
    robo.desenhar(janela)
    pygame.display.flip()

pygame.quit()
