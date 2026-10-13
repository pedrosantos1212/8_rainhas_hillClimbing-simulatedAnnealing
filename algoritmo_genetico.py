
import random

from oito_rainhas import (
    calcular_conflitos,
    criar_tabuleiro,
    mostrar_tabuleiro
)


def criar_populacao(tamanho_populacao=100, tamanho_tabuleiro=8):
    """Cria uma lista de tabuleiros aleatorios."""
    populacao = []

    for _ in range(tamanho_populacao):
        individuo = criar_tabuleiro(tamanho_tabuleiro)
        populacao.append(individuo)

    return populacao


def calcular_fitness(individuo):
    """Quanto maior o fitness, melhor o individuo."""
    total_pares = len(individuo) * (len(individuo) - 1) // 2
    conflitos = calcular_conflitos(individuo)

    return total_pares - conflitos


def selecionar_pai(populacao, tamanho_torneio=5):
    """Seleciona um pai por torneio."""
    participantes = random.sample(
        populacao,
        min(tamanho_torneio, len(populacao))
    )

    return max(participantes, key=calcular_fitness)


def cruzar(pai1, pai2):
    """Combina partes dos dois pais para gerar um filho."""
    tamanho = len(pai1)

    if tamanho < 2:
        return pai1.copy()

    ponto_corte = random.randint(1, tamanho - 1)

    filho = pai1[:ponto_corte] + pai2[ponto_corte:]

    return filho


def mutar(individuo, taxa_mutacao=0.10):
    """Muda aleatoriamente a linha de uma rainha."""
    mutante = individuo.copy()
    tamanho = len(mutante)

    for coluna in range(tamanho):
        if random.random() < taxa_mutacao:
            linha_atual = mutante[coluna]
            nova_linha = random.randrange(tamanho - 1)

            # Garante uma linha diferente da atual.
            if nova_linha >= linha_atual:
                nova_linha += 1

            mutante[coluna] = nova_linha

    return mutante


def algoritmo_genetico(
    tamanho_populacao=100,
    tamanho_tabuleiro=8,
    max_geracoes=1000,
    taxa_mutacao=0.10,
    tamanho_torneio=5,
    mostrar_logs=True
):
    """Executa o algoritmo genetico."""
    if tamanho_populacao < 2:
        raise ValueError("A populacao deve ter pelo menos 2 individuos.")

    if tamanho_tabuleiro < 2:
        raise ValueError("O tabuleiro deve ter pelo menos 2 rainhas.")

    if max_geracoes < 0:
        raise ValueError("O numero maximo de geracoes nao pode ser negativo.")

    if not 0 <= taxa_mutacao <= 1:
        raise ValueError("A taxa de mutacao deve estar entre 0 e 1.")

    populacao = criar_populacao(
        tamanho_populacao,
        tamanho_tabuleiro
    )

    melhor_individuo = min(
        populacao,
        key=calcular_conflitos
    ).copy()

    melhor_fitness = calcular_fitness(melhor_individuo)
    geracao_final = 0

    if mostrar_logs:
        print(
            "Geracao 0 | Melhor fitness:",
            melhor_fitness,
            "| Conflitos:",
            calcular_conflitos(melhor_individuo)
        )

    # Verifica a populacao inicial.
    if calcular_conflitos(melhor_individuo) == 0:
        return melhor_individuo, 0

    for geracao in range(1, max_geracoes + 1):
        nova_populacao = []

        # Elitismo: preserva o melhor individuo atual.
        melhor_da_geracao = min(
            populacao,
            key=calcular_conflitos
        )

        nova_populacao.append(melhor_da_geracao.copy())

        # Cria filhos ate completar a populacao.
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecionar_pai(populacao, tamanho_torneio)
            pai2 = selecionar_pai(populacao, tamanho_torneio)

            filho = cruzar(pai1, pai2)
            filho = mutar(filho, taxa_mutacao)

            nova_populacao.append(filho)

        populacao = nova_populacao
        geracao_final = geracao

        # Avalia a nova geracao.
        melhor_da_geracao = min(
            populacao,
            key=calcular_conflitos
        )

        conflitos = calcular_conflitos(melhor_da_geracao)
        fitness = calcular_fitness(melhor_da_geracao)

        if fitness > melhor_fitness:
            melhor_individuo = melhor_da_geracao.copy()
            melhor_fitness = fitness

        if mostrar_logs and (geracao % 10 == 0 or conflitos == 0):
            print(
                f"Geracao {geracao} | "
                f"Melhor fitness: {fitness} | "
                f"Conflitos: {conflitos}"
            )

        # Encerra quando encontra uma solucao perfeita.
        if conflitos == 0:
            melhor_individuo = melhor_da_geracao.copy()
            break

    return melhor_individuo, geracao_final


if __name__ == "__main__":
    # Permite repetir os testes com a mesma sequencia aleatoria.
    random.seed(42)

    solucao, geracoes = algoritmo_genetico(
        tamanho_populacao=100,
        tamanho_tabuleiro=8,
        max_geracoes=1000,
        taxa_mutacao=0.10,
        tamanho_torneio=5,
        mostrar_logs=True
    )

    conflitos_finais = calcular_conflitos(solucao)

    print("\nMelhor tabuleiro encontrado:")
    print(solucao)
    mostrar_tabuleiro(solucao)

    print("\nConflitos finais:", conflitos_finais)
    print("Geracao em que terminou:", geracoes)

    if conflitos_finais == 0:
        print("Solucao encontrada! Nenhuma rainha ataca outra.")
    else:
        print(
            "Nao foi encontrada uma solucao "
            "dentro do limite de geracoes."
        )
