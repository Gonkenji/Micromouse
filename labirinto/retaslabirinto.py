for linhas in range(1,N_LINHAS+1):
    for colunas in range(1,N_LINHAS+1):
        objetivo.append(((TAM_CELULA/2+MARGEM)*colunas,(TAM_CELULA/2 + MARGEM)*linhas))
        continue

def remover_restos(pontos):
    if len(pontos) <= 2:
        return pontos[:]  # nada a remover

    resultado = [pontos[0]]

    for i in range(1, len(pontos)-1):
        p_ant = pontos[i-1]
        p     = pontos[i]
        p_prox = pontos[i+1]

        # Vetor antes e depois
        dx1, dy1 = p[0] - p_ant[0], p[1] - p_ant[1]
        dx2, dy2 = p_prox[0] - p[0], p_prox[1] - p[1]

        # Se direção muda, mantemos o ponto
        if (dx1, dy1) != (dx2, dy2):
            resultado.append(p)

    resultado.append(pontos[-1])  # sempre manter o último
    return resultado

objetivo = remover_restos(objetivo)
