"""Interface visual no terminal para comparar os dois algoritmos."""

import os
import time

from hillClimbing import hill_climbing
from oito_rainhas import calcular_conflitos
from oito_rainhas import criar_tabuleiro
from oito_rainhas import mostrar_tabuleiro
from simulatedAnnealing import simulated_annealing


SIMULATED_ANNEALING = "Simulated Annealing"
HILL_CLIMBING = "Hill Climbing"


def limpar_terminal():
    """Apaga a tela antes de desenhar o proximo estado."""
    # No Windows usamos "cls". Em Linux e macOS usamos "clear".
    os.system("cls" if os.name == "nt" else "clear")


def exibir_estado(titulo, tabuleiro):
    """Mostra a lista, o desenho e os conflitos de um estado."""
    print(f"\n{titulo}")
    print("Posicoes:", tabuleiro)
    mostrar_tabuleiro(tabuleiro)
    print("Conflitos:", calcular_conflitos(tabuleiro))


def exibir_passo(passo, numero, total, algoritmo):
    """Desenha um estado aceito durante a busca."""
    limpar_terminal()

    print("=" * 58)
    print(f" {algoritmo.upper()} - ANIMACAO NO TERMINAL")
    print("=" * 58)
    print(f"Passo visual: {numero}/{total}")
    print(f"Iteracao do algoritmo: {passo['iteracao']}")

    # Somente o Simulated Annealing possui temperatura.
    if "temperatura" in passo:
        print(f"Temperatura: {passo['temperatura']:.4f}")

    print(f"Evento: {passo['evento']}")
    print(
        "Conflitos: "
        f"{passo['conflitos_antes']} -> {passo['conflitos_depois']}"
    )
    print()

    mostrar_tabuleiro(passo["tabuleiro"])
    print("\nPosicoes:", passo["tabuleiro"])


def animar_historico(
    historico,
    algoritmo,
    automatico=True,
    atraso=0.10
):
    """Reproduz o historico automaticamente ou passo a passo."""
    total = len(historico)

    for numero, passo in enumerate(historico, start=1):
        exibir_passo(passo, numero, total, algoritmo)

        if automatico:
            # A pausa deixa o movimento visivel no terminal.
            time.sleep(atraso)
        else:
            comando = input("\nEnter avanca | Q encerra a animacao: ").strip()
            if comando.lower() == "q":
                break


def executar_algoritmo(tabuleiro_inicial, algoritmo, modo="rapido"):
    """Executa um algoritmo nos modos rapido, automatico ou passo a passo."""
    # A interface pede o historico apenas quando precisa anima-lo.
    guardar_historico = modo in ("automatico", "passo")
    historico = [] if guardar_historico else None

    print(f"\nExecutando {algoritmo}...")

    if algoritmo == SIMULATED_ANNEALING:
        final, iteracoes, pioras = simulated_annealing(
            tabuleiro_inicial,
            historico=historico,
            mostrar_logs=False
        )
        resolveu = calcular_conflitos(final) == 0
    else:
        final, iteracoes, resolveu = hill_climbing(
            tabuleiro_inicial,
            historico=historico,
            mostrar_logs=False
        )
        pioras = None

    if modo == "automatico":
        # O Hill Climbing costuma ter poucos passos e pode ser mais lento.
        atraso = 0.45 if algoritmo == HILL_CLIMBING else 0.08
        animar_historico(
            historico,
            algoritmo,
            automatico=True,
            atraso=atraso
        )
    elif modo == "passo":
        animar_historico(historico, algoritmo, automatico=False)

    # Limpa a animacao e deixa o resumo final na tela.
    if guardar_historico:
        limpar_terminal()

    exibir_estado("Estado inicial", tabuleiro_inicial)
    exibir_estado("Estado final", final)

    if algoritmo == HILL_CLIMBING:
        print("Passos realizados:", iteracoes)
    else:
        print("Iteracoes:", iteracoes)
        print("Pioras aceitas:", pioras)

    if resolveu:
        print("Resultado: solucao encontrada!")
    elif algoritmo == HILL_CLIMBING:
        print("Resultado: busca encerrada em um minimo local.")
    else:
        print("Resultado: terminou sem encontrar uma solucao.")

    return {
        "final": final,
        "iteracoes": iteracoes,
        "resolveu": resolveu,
        "pioras": pioras
    }


def comparar_algoritmos(tabuleiro_inicial):
    """Executa os dois algoritmos a partir do mesmo estado inicial."""
    # Os logs ficam desligados para mostrar apenas a tabela comparativa.
    final_hill, passos_hill, resolveu_hill = hill_climbing(
        tabuleiro_inicial,
        mostrar_logs=False
    )
    final_sa, iteracoes_sa, pioras_sa = simulated_annealing(
        tabuleiro_inicial,
        mostrar_logs=False
    )
    resolveu_sa = calcular_conflitos(final_sa) == 0

    limpar_terminal()
    exibir_estado("Mesmo estado inicial para os dois", tabuleiro_inicial)

    print("\nCOMPARACAO")
    print("-" * 72)
    print(f"{'Algoritmo':<24}{'Conflitos':>12}{'Passos/Iter.':>16}{'Solucao':>12}")
    print("-" * 72)
    print(
        f"{HILL_CLIMBING:<24}"
        f"{calcular_conflitos(final_hill):>12}"
        f"{passos_hill:>16}"
        f"{('Sim' if resolveu_hill else 'Nao'):>12}"
    )
    print(
        f"{SIMULATED_ANNEALING:<24}"
        f"{calcular_conflitos(final_sa):>12}"
        f"{iteracoes_sa:>16}"
        f"{('Sim' if resolveu_sa else 'Nao'):>12}"
    )
    print("-" * 72)
    print("Pioras aceitas pelo Simulated Annealing:", pioras_sa)


def mostrar_menu():
    """Mostra as opcoes disponiveis."""
    print("\n=== SIMULADOR DAS 8 RAINHAS ===")
    print("1 - Gerar novo tabuleiro")
    print("2 - Mostrar tabuleiro atual")
    print("3 - Simulated Annealing: executar rapidamente")
    print("4 - Simulated Annealing: animar automaticamente")
    print("5 - Simulated Annealing: visualizar passo a passo")
    print("6 - Hill Climbing: executar rapidamente")
    print("7 - Hill Climbing: animar automaticamente")
    print("8 - Hill Climbing: visualizar passo a passo")
    print("9 - Comparar os dois algoritmos")
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
            executar_algoritmo(
                tabuleiro_atual,
                SIMULATED_ANNEALING,
                modo="rapido"
            )

        elif opcao == "4":
            executar_algoritmo(
                tabuleiro_atual,
                SIMULATED_ANNEALING,
                modo="automatico"
            )

        elif opcao == "5":
            executar_algoritmo(
                tabuleiro_atual,
                SIMULATED_ANNEALING,
                modo="passo"
            )

        elif opcao == "6":
            executar_algoritmo(
                tabuleiro_atual,
                HILL_CLIMBING,
                modo="rapido"
            )

        elif opcao == "7":
            executar_algoritmo(
                tabuleiro_atual,
                HILL_CLIMBING,
                modo="automatico"
            )

        elif opcao == "8":
            executar_algoritmo(
                tabuleiro_atual,
                HILL_CLIMBING,
                modo="passo"
            )

        elif opcao == "9":
            comparar_algoritmos(tabuleiro_atual)

        elif opcao == "0":
            print("Simulador encerrado.")
            break

        else:
            print("Opcao invalida. Digite um numero mostrado no menu.")


if __name__ == "__main__":
    main()
