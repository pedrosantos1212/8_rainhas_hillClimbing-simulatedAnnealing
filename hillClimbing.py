"""
Hill Climbing (Subida da Encosta) para o problema das 8 Rainhas.

Ideia: a cada passo, olha todos os vizinhos (mover UMA rainha dentro da
coluna dela) e vai para o que tiver MENOS conflitos.

Se nenhum vizinho for melhor que o atual, o algoritmo trava (máximo local).
"""
# puxa as funções prontas do oito_rainhas.py (N = 8, o tamanho do tabuleiro)
from oito_rainhas import N, criar_tabuleiro, contar_conflitos, imprimir_tabuleiro


def gerar_vizinhos(tabuleiro):
    """Gera os 56 vizinhos: cada rainha vai para cada outra linha da sua coluna."""
    vizinhos = []
    for coluna in range(N):
        for linha in range(N):
            # pula a linha onde a rainha já tá, senão nn mexeu nada 
            if linha != tabuleiro[coluna]:
                # copy pra nn estragar o tabuleiro original 
                vizinho = tabuleiro.copy()
                vizinho[coluna] = linha
                vizinhos.append(vizinho)
    # 8 colunas x 7 linhas = 56 vizinhos
    return vizinhos


def hill_climbing(tabuleiro):
    """Roda o Hill Climbing. Retorna (tabuleiro_final, passos, resolveu)."""
    passos = 0

    while True:
        conflitos_atual = contar_conflitos(tabuleiro)

        # 0 conflitos = deu certo
        if conflitos_atual == 0:
            return tabuleiro, passos, True

        # procura o melhor vizinho (começa achando que o melhor é o atual)
        melhor = tabuleiro
        melhor_conflitos = conflitos_atual
        for vizinho in gerar_vizinhos(tabuleiro):
            c = contar_conflitos(vizinho)
            if c < melhor_conflitos:
                melhor = vizinho
                melhor_conflitos = c

        # nenhum vizinho melhor = travou (máximo local)
        if melhor_conflitos >= conflitos_atual:
            return tabuleiro, passos, False

        # achou um melhor, continua
        tabuleiro = melhor
        passos += 1
        print(f"Passo {passos}: {conflitos_atual} -> {melhor_conflitos} conflitos")


# só roda quando executa esse arquivo direto
# se outro arquivo importar, esse bloco nn roda
if __name__ == "__main__":
    inicial = criar_tabuleiro()
    print("Tabuleiro inicial:", inicial, "| conflitos:", contar_conflitos(inicial))
    imprimir_tabuleiro(inicial)

    final, passos, resolveu = hill_climbing(inicial)

    if resolveu:
        print(f"Solução encontrada em {passos} passos!")
    else:
        print(f"Travou no máximo local com {contar_conflitos(final)} conflitos.")
    print("Tabuleiro final:", final)
    imprimir_tabuleiro(final)