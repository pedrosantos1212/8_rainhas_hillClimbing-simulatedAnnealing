from pathlib import Path

code = """Interface visual no terminal para o algoritmo genetico das 8 rainhas."""

import os
import random
import time

from oito_rainhas import (
    calcular_conflitos,
    criar_tabuleiro,
    mostrar_tabuleiro
)
from algoritmo_genetico import (
    criar_populacao,
    calcular_fitness,
    selecionar_pai,
    cruzar,
    mutar
)


def limpar_terminal():
    """Apaga a tela antes de desenhar o proximo estado."""
    os.system("cls" if os.name == "nt" else "clear")


def exibir_estado(titulo, tabuleiro):
    """Mostra a lista, o desenho e os conflitos de um individuo."""
    print(f"\\n{titulo}")
    print("Posicoes:", tabuleiro)
    mostrar_tabuleiro(tabuleiro)
    print("Conflitos:", calcular_conflitos(tabuleiro))
    print("Fitness:", calcular_fitness(tabuleiro))


def exibir_passo(passo, numero, total):
    """Desenha o melhor individuo registrado em uma geracao."""
    limpar_terminal()

    print("=" * 56)
    print(" ALGORITMO GENETICO - ANIMACAO NO TERMINAL")
    print("=" * 56)
    print(f"Passo visual: {numero}/{total}")
    print(f"Geracao: {passo['geracao']}")
    print(f"Melhor fitness: {passo['fitness']}")
    print(f"Conflitos: {passo['conflitos']}")
    print(f"Individuo: {passo['tabuleiro']}")
    print()

    mostrar_tabuleiro(passo["tabuleiro"])


def animar_historico(historico, automatico=True, atraso=0.15):
    """Reproduz o historico automaticamente ou passo a passo."""
    total = len(historico)

    for numero, passo in enumerate(historico, start=1):
        exibir_passo(passo, numero, total)

        if automatico:
            time.sleep(atraso)
        else:
            comando = input("\\nEnter avanca | Q encerra a animacao: ").strip()
            if comando.lower() == "q":
                break


def executar_algoritmo_genetico(
    tabuleiro_inicial=None,
    modo="rapido",
    tamanho_populacao=100,
    max_geracoes=1000,
    taxa_mutacao=0.10,
    tamanho_torneio=5
):
    """Executa o algoritmo genetico e registra o melhor individuo por geracao."""
    tamanho_tabuleiro = (
        len(tabuleiro_inicial) if tabuleiro_inicial is not None else 8
    )

    # A populacao inicial e aleatoria. Se o usuario informou um tabuleiro,
    # ele substitui o primeiro individuo para que participe da busca.
    populacao = criar_populacao(tamanho_populacao, tamanho_tabuleiro)

    if tabuleiro_inicial is not None:
        populacao[0] = tabuleiro_inicial.copy()

    historico = []
    melhor = min(populacao, key=calcular_conflitos).copy()

    historico.append({
        "tabuleiro": melhor.copy(),
        "geracao": 0,
        "conflitos": calcular_conflitos(melhor),
        "fitness": calcular_fitness(melhor)
    })

    geracao_final = 0

    if calcular_conflitos(melhor) == 0:
        return melhor, geracao_final, historico

    for geracao in range(1, max_geracoes + 1):
        nova_populacao = []

        # Elitismo: preserva o melhor individuo da geracao atual.
        melhor_atual = min(populacao, key=calcular_conflitos)
        nova_populacao.append(melhor_atual.copy())

        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecionar_pai(populacao, tamanho_torneio)
            pai2 = selecionar_pai(populacao, tamanho_torneio)

            filho = cruzar(pai1, pai2)
            filho = mutar(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao
        geracao_final = geracao

        melhor_geracao = min(populacao, key=calcular_conflitos)
        conflitos = calcular_conflitos(melhor_geracao)
        fitness = calcular_fitness(melhor_geracao)

        # O elitismo preserva a melhor solucao, mas guardamos o melhor
        # encontrado em todo o processo para o resumo final.
        if calcular_conflitos(melhor_geracao) < calcular_conflitos(melhor):
            melhor = melhor_geracao.copy()

        # Guarda apenas melhorias, empates no melhor global ou a solucao final,
        # para que a animacao mostre a evolucao sem repetir cada geracao igual.
        if (
            fitness >= calcular_fitness(historico[-1]["tabuleiro"])
            or conflitos == 0
        ):
            historico.append({
                "tabuleiro": melhor_geracao.copy(),
                "geracao": geracao,
                "conflitos": conflitos,
                "fitness": fitness
            })

        if conflitos == 0:
            melhor = melhor_geracao.copy()
            break

    # Garante que a animacao termine mostrando a melhor solucao encontrada.
    if not historico or historico[-1]["tabuleiro"] != melhor:
        historico.append({
            "tabuleiro": melhor.copy(),
            "geracao": geracao_final,
            "conflitos": calcular_conflitos(melhor),
            "fitness": calcular_fitness(melhor)
        })

    if modo == "automatico":
        animar_historico(historico, automatico=True)
    elif modo == "passo":
        animar_historico(historico, automatico=False)

    if modo in ("automatico", "passo"):
        limpar_terminal()

    print("\\nParametros utilizados:")
    print("Tamanho da populacao:", tamanho_populacao)
    print("Maximo de geracoes:", max_geracoes)
    print("Taxa de mutacao:", taxa_mutacao)
    print("Tamanho do torneio:", tamanho_torneio)

    exibir_estado("Melhor solucao encontrada", melhor)
    print("Geracoes executadas:", geracao_final)

    if calcular_conflitos(melhor) == 0:
        print("Resultado: solucao encontrada!")
    else:
        print("Resultado: terminou sem encontrar uma solucao.")

    return melhor


def mostrar_menu():
    """Mostra as opcoes disponiveis."""
    print("\\n=== SIMULADOR GENETICO DAS 8 RAINHAS ===")
    print("1 - Gerar novo tabuleiro")
    print("2 - Mostrar tabuleiro atual")
    print("3 - Executar rapidamente")
    print("4 - Animar automaticamente")
    print("5 - Visualizar passo a passo")
    print("0 - Sair")


def main():
    """Mantem o menu aberto ate o usuario escolher sair."""
    tabuleiro_atual = criar_tabuleiro()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            tabuleiro_atual = criar_tabuleiro()
            exibir_estado("Novo tabuleiro", tabuleiro_atual)

        elif opcao == "2":
            exibir_estado("Tabuleiro atual", tabuleiro_atual)

        elif opcao == "3":
            executar_algoritmo_genetico(tabuleiro_atual, modo="rapido")

        elif opcao == "4":
            executar_algoritmo_genetico(tabuleiro_atual, modo="automatico")

        elif opcao == "5":
            executar_algoritmo_genetico(tabuleiro_atual, modo="passo")

        elif opcao == "0":
            print("Simulador encerrado.")
            break

        else:
            print("Opcao invalida. Digite um numero mostrado no menu.")


if __name__ == "__main__":
    main()

