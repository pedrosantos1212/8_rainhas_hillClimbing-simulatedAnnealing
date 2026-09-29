"""Interface visual no terminal para o problema das 8 rainhas."""

import os
import time

from oito_rainhas import calcular_conflitos
from oito_rainhas import criar_tabuleiro
from oito_rainhas import mostrar_tabuleiro
from simulatedAnnealing import simulated_annealing


def limpar_terminal():
    """Apaga a tela antes de desenhar o proximo estado."""
    # O projeto roda no Windows, onde o comando de limpeza e "cls".
    # O segundo comando permite executar o projeto em Linux ou macOS.
    os.system("cls" if os.name == "nt" else "clear")


def exibir_estado(titulo, tabuleiro):
    """Mostra a lista, o desenho e os conflitos de um estado."""
    print(f"\n{titulo}")
    print("Posicoes:", tabuleiro)
    mostrar_tabuleiro(tabuleiro)
    print("Conflitos:", calcular_conflitos(tabuleiro))


def exibir_passo(passo, numero, total):
    """Desenha um estado aceito durante a busca."""
    limpar_terminal()

    print("=" * 52)
    print(" SIMULATED ANNEALING - ANIMACAO NO TERMINAL")
    print("=" * 52)
    print(f"Passo visual: {numero}/{total}")
    print(f"Iteracao do algoritmo: {passo['iteracao']}")
    print(f"Temperatura: {passo['temperatura']:.4f}")
    print(f"Evento: {passo['evento']}")
    print(
        "Conflitos: "
        f"{passo['conflitos_antes']} -> {passo['conflitos_depois']}"
    )
    print()

    mostrar_tabuleiro(passo["tabuleiro"])
    print("\nPosicoes:", passo["tabuleiro"])


def animar_historico(historico, automatico=True, atraso=0.10):
    """Reproduz o historico automaticamente ou passo a passo."""
    total = len(historico)

    for numero, passo in enumerate(historico, start=1):
        exibir_passo(passo, numero, total)

        if automatico:
            # Pequena pausa para que a mudanca do tabuleiro fique visivel.
            time.sleep(atraso)
        else:
            comando = input("\nEnter avanca | Q encerra a animacao: ").strip()
            if comando.lower() == "q":
                break


def executar_simulated_annealing(tabuleiro_inicial, modo="rapido"):
    """Executa o algoritmo e, quando solicitado, anima seus estados."""
    # A lista e preenchida pelo algoritmo sem alterar o retorno da funcao.
    historico = []
    guardar_historico = modo in ("automatico", "passo")

    print("\nExecutando Simulated Annealing...")
    final, iteracoes, pioras = simulated_annealing(
        tabuleiro_inicial,
        historico=historico if guardar_historico else None,
        # A animacao mostra as pioras, entao evitamos textos duplicados.
        mostrar_logs=False
    )

    if modo == "automatico":
        animar_historico(historico, automatico=True)
    elif modo == "passo":
        animar_historico(historico, automatico=False)

    # Limpa a animacao e deixa o resumo final na tela.
    if guardar_historico:
        limpar_terminal()

    exibir_estado("Estado inicial", tabuleiro_inicial)
    exibir_estado("Estado final", final)
    print("Iteracoes:", iteracoes)
    print("Pioras aceitas:", pioras)

    if calcular_conflitos(final) == 0:
        print("Resultado: solucao encontrada!")
    else:
        print("Resultado: terminou sem encontrar uma solucao.")


def mostrar_menu():
    """Mostra as opcoes disponiveis."""
    print("\n=== SIMULADOR DAS 8 RAINHAS ===")
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
            executar_simulated_annealing(tabuleiro_atual, modo="rapido")

        elif opcao == "4":
            executar_simulated_annealing(tabuleiro_atual, modo="automatico")

        elif opcao == "5":
            executar_simulated_annealing(tabuleiro_atual, modo="passo")

        elif opcao == "0":
            print("Simulador encerrado.")
            break

        else:
            print("Opcao invalida. Digite um numero mostrado no menu.")


if __name__ == "__main__":
    main()
