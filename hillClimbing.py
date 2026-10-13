"""Hill Climbing para o problema das 8 rainhas."""

# 1. Importa as funcoes compartilhadas do tabuleiro.
from oito_rainhas import calcular_conflitos
from oito_rainhas import criar_tabuleiro
from oito_rainhas import mostrar_tabuleiro


# 2. Gera todos os movimentos possiveis a partir de um estado.
def gerar_vizinhos(tabuleiro):
    """Gera todos os tabuleiros obtidos ao mover uma rainha."""
    tamanho = len(tabuleiro)
    vizinhos = []

    for coluna in range(tamanho):
        for linha in range(tamanho):
            # A linha atual nao gera um movimento.
            if linha != tabuleiro[coluna]:
                # A copia preserva o tabuleiro original.
                vizinho = tabuleiro.copy()
                vizinho[coluna] = linha
                vizinhos.append(vizinho)

    # Para 8 rainhas: 8 colunas vezes 7 novas linhas = 56 vizinhos.
    return vizinhos


# 3. Executa a busca escolhendo sempre o melhor vizinho.
def hill_climbing(
    tabuleiro_inicial,
    historico=None,
    mostrar_logs=True
):
    """Retorna (tabuleiro_final, movimentos_realizados, resolveu)."""
    # Trabalha em uma copia para preservar o estado inicial.
    atual = tabuleiro_inicial.copy()
    passos = 0

    # A interface pode enviar uma lista para guardar a animacao.
    # Isso nao muda os tres valores retornados pela funcao.
    if historico is not None:
        conflitos_iniciais = calcular_conflitos(atual)
        historico.append({
            "tabuleiro": atual.copy(),
            "iteracao": 0,
            "conflitos_antes": conflitos_iniciais,
            "conflitos_depois": conflitos_iniciais,
            "evento": "Estado inicial"
        })

    while True:
        conflitos_atual = calcular_conflitos(atual)

        # Caso 1: encontrou a solucao.
        if conflitos_atual == 0:
            return atual, passos, True

        melhor = atual
        melhor_conflitos = conflitos_atual

        # Avalia todos os vizinhos e mantem o de menor custo.
        # Em caso de empate, mantem o primeiro encontrado.
        for vizinho in gerar_vizinhos(atual):
            conflitos_vizinho = calcular_conflitos(vizinho)

            if conflitos_vizinho < melhor_conflitos:
                melhor = vizinho
                melhor_conflitos = conflitos_vizinho

        # Caso 2: sem melhora estrita, encerra em um minimo local.
        if melhor_conflitos >= conflitos_atual:
            return atual, passos, False

        # Caso 3: encontrou uma melhora e continua a busca.
        atual = melhor
        passos += 1

        if historico is not None:
            historico.append({
                "tabuleiro": atual.copy(),
                "iteracao": passos,
                "conflitos_antes": conflitos_atual,
                "conflitos_depois": melhor_conflitos,
                "evento": "Melhor vizinho aceito"
            })

        if mostrar_logs:
            print(
                f"Passo {passos}: "
                f"{conflitos_atual} -> {melhor_conflitos} conflitos"
            )


# 4. Executa uma demonstracao quando o arquivo e aberto diretamente.
if __name__ == "__main__":
    inicial = criar_tabuleiro()

    print(
        "Tabuleiro inicial:", inicial,
        "| conflitos:", calcular_conflitos(inicial)
    )
    mostrar_tabuleiro(inicial)

    final, passos, resolveu = hill_climbing(inicial)

    # 5. Mostra o resultado da busca.
    if resolveu:
        print(f"Solucao encontrada em {passos} passos!")
    else:
        print(
            "Busca parou em um minimo local. "
            f"Restaram {calcular_conflitos(final)} conflitos."
        )

    print("Tabuleiro final:", final)
    mostrar_tabuleiro(final)
