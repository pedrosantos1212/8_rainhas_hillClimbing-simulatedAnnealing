"""
Hill Climbing (Subida da Encosta) para o problema das 8 Rainhas.

"""

from oito_rainhas import criar_tabuleiro, calcular_conflitos, mostrar_tabuleiro


def gerar_vizinhos(tabuleiro):
    """Gera tamanho * (tamanho - 1) vizinhos; para 8 rainhas, são 56."""
    tamanho = len(tabuleiro)
    vizinhos = []

    for coluna in range(tamanho):
        for linha in range(tamanho):
            # A posição atual não gera um movimento.
            if linha != tabuleiro[coluna]:
                # Copia a lista para preservar o tabuleiro original.
                vizinho = tabuleiro.copy()
                vizinho[coluna] = linha
                vizinhos.append(vizinho)

    return vizinhos


def hill_climbing(tabuleiro):
    """Retorna (tabuleiro_final, movimentos_realizados, resolveu)."""
    passos = 0

    while True:
        conflitos_atual = calcular_conflitos(tabuleiro)

        # Zero conflitos significa que nenhuma rainha ataca outra.
        if conflitos_atual == 0:
            return tabuleiro, passos, True

        melhor = tabuleiro
        melhor_conflitos = conflitos_atual

        # Avalia todos os vizinhos e mantém o de menor custo.
        # Em caso de empate, mantém o primeiro encontrado.
        for vizinho in gerar_vizinhos(tabuleiro):
            conflitos_vizinho = calcular_conflitos(vizinho)

            if conflitos_vizinho < melhor_conflitos:
                melhor = vizinho
                melhor_conflitos = conflitos_vizinho

        # Sem melhora estrita, para mesmo que ainda existam conflitos.
        if melhor_conflitos >= conflitos_atual:
            return tabuleiro, passos, False

        tabuleiro = melhor
        passos += 1
        print(
            f"Passo {passos}: "
            f"{conflitos_atual} -> {melhor_conflitos} conflitos"
        )


if __name__ == "__main__":
    inicial = criar_tabuleiro()
    print(
        "Tabuleiro inicial:", inicial,
        "| conflitos:", calcular_conflitos(inicial)
    )
    mostrar_tabuleiro(inicial)

    final, passos, resolveu = hill_climbing(inicial)

    if resolveu:
        print(f"Solução encontrada em {passos} passos!")
    else:
        print(
            "Busca parou sem vizinho com menos conflitos. "
            f"Restaram {calcular_conflitos(final)} conflitos."
        )

    print("Tabuleiro final:", final)
    mostrar_tabuleiro(final)
