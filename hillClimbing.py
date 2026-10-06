"""
Hill Climbing (Subida da Encosta) para o problema das 8 Rainhas.

"""
# 1. IMPORTA AS FUNÇÕES AUXILIARES
from oito_rainhas import criar_tabuleiro, calcular_conflitos, mostrar_tabuleiro

# 2. GERA OS MOVIMENTOS POSSÍVEIS
def gerar_vizinhos(tabuleiro):
    #Gera tamanho * (tamanho - 1) vizinhos; para 8 rainhas, são 56.
    tamanho = len(tabuleiro)
    vizinhos = []
    # Escolhe uma coluna de cada vez.
    for coluna in range(tamanho):
        for linha in range(tamanho):
            # A posição atual não gera um movimento.
            if linha != tabuleiro[coluna]:
                # Copia a lista para preservar o tabuleiro original.
                vizinho = tabuleiro.copy()
                vizinho[coluna] = linha
                vizinhos.append(vizinho)

    return vizinhos

# 3. EXECUTA A BUSCA HILL CLIMBING
def hill_climbing(tabuleiro):
    # Retorna (tabuleiro_final, movimentos_realizados, resolveu)
    passos = 0

    while True:
        conflitos_atual = calcular_conflitos(tabuleiro)

        # CASO 1: encontrou a solução.
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

         # CASO 2: não encontrou nenhuma opção com menos conflitos
        if melhor_conflitos >= conflitos_atual:
            return tabuleiro, passos, False

        # CASO 3: encontrou uma melhora.
        tabuleiro = melhor
        passos += 1
        print(
            f"Passo {passos}: "
            f"{conflitos_atual} -> {melhor_conflitos} conflitos"
        )

# 4. PREPARA E INICIA A DEMONSTRAÇÃO
if __name__ == "__main__":
    inicial = criar_tabuleiro()

     # Exibe a lista de posições e a quantidade inicial de conflitos.
    print(
        "Tabuleiro inicial:", inicial,
        "| conflitos:", calcular_conflitos(inicial)
    )
    mostrar_tabuleiro(inicial)

    final, passos, resolveu = hill_climbing(inicial)


    # 5. MOSTRA O RESULTADO DA BUSCA
    if resolveu:
        print(f"Solução encontrada em {passos} passos!")
    else:
        print(
            "Busca parou sem vizinho com menos conflitos. "
            f"Restaram {calcular_conflitos(final)} conflitos."
        )


    # Exibe as posições finais e desenha o tabuleiro.
    print("Tabuleiro final:", final)
    mostrar_tabuleiro(final)
