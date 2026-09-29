import math
import random

from oito_rainhas import calcular_conflitos
from oito_rainhas import criar_tabuleiro
from oito_rainhas import mostrar_tabuleiro


def gerar_vizinho(tabuleiro):
    # A copia permite rejeitar o vizinho sem alterar o estado atual.
    vizinho = tabuleiro.copy()

    # Escolhe qual rainha sera movimentada pela coluna dela.
    coluna = random.randrange(len(tabuleiro))
    linha_atual = vizinho[coluna]

    # Sorteia uma linha diferente para a rainha escolhida.
    nova_linha = random.randrange(len(tabuleiro))
    while nova_linha == linha_atual:
        nova_linha = random.randrange(len(tabuleiro))

    # Faz o movimento somente na copia.
    vizinho[coluna] = nova_linha

    return vizinho


def simulated_annealing(
    tabuleiro_inicial,
    temperatura=100.0,
    taxa_resfriamento=0.99,
    temperatura_minima=0.001,
    max_iteracoes=10000,
    historico=None,
    mostrar_logs=True
):
    # Preserva o tabuleiro inicial para a comparacao final.
    atual = tabuleiro_inicial.copy()
    iteracao = 0
    pioras_aceitas = 0

    # A interface pode enviar uma lista para guardar os estados aceitos.
    # Isso nao muda os tres valores retornados pela funcao.
    if historico is not None:
        historico.append({
            "tabuleiro": atual.copy(),
            "iteracao": 0,
            "temperatura": temperatura,
            "conflitos_antes": calcular_conflitos(atual),
            "conflitos_depois": calcular_conflitos(atual),
            "evento": "Estado inicial"
        })

    # Continua enquanto ainda houver temperatura e tentativas.
    while (
        temperatura > temperatura_minima
        and iteracao < max_iteracoes
    ):
        conflitos_atual = calcular_conflitos(atual)

        # Zero conflitos significa que encontramos uma solucao.
        if conflitos_atual == 0:
            break

        # Tenta mover uma rainha e mede o novo tabuleiro.
        vizinho = gerar_vizinho(atual)
        conflitos_vizinho = calcular_conflitos(vizinho)

        # Negativo melhora, zero empata e positivo piora.
        delta = conflitos_vizinho - conflitos_atual
        evento = ""
        aceitou = False

        # Melhorias e empates sao sempre aceitos.
        if delta <= 0:
            atual = vizinho
            aceitou = True

            if delta < 0:
                evento = "Melhoria aceita"
            else:
                evento = "Empate aceito"

        else:
            # A temperatura define a chance de aceitar uma piora.
            probabilidade = math.exp(-delta / temperatura)
            sorteio = random.random()

            if sorteio < probabilidade:
                atual = vizinho
                aceitou = True
                evento = "Estado pior aceito"
                pioras_aceitas += 1

                if mostrar_logs:
                    print(
                        f"Iteracao {iteracao}: estado pior aceito "
                        f"({conflitos_atual} -> {conflitos_vizinho} conflitos)"
                    )

        # Guarda apenas os movimentos aceitos para a animacao do terminal.
        if aceitou and historico is not None:
            historico.append({
                # A copia impede que este estado mude nas proximas iteracoes.
                "tabuleiro": atual.copy(),
                "iteracao": iteracao + 1,
                "temperatura": temperatura,
                "conflitos_antes": conflitos_atual,
                "conflitos_depois": conflitos_vizinho,
                "evento": evento
            })

        # Esfria depois de cada tentativa.
        temperatura = temperatura * taxa_resfriamento
        iteracao += 1

    return atual, iteracao, pioras_aceitas


if __name__ == "__main__":
    # Teste simples do algoritmo.
    inicial = criar_tabuleiro()

    final, iteracoes, pioras = simulated_annealing(inicial)

    print("\nTabuleiro inicial:")
    print(inicial)
    mostrar_tabuleiro(inicial)
    print("Conflitos iniciais:", calcular_conflitos(inicial))

    print("\nTabuleiro final:")
    print(final)
    mostrar_tabuleiro(final)
    print("Conflitos finais:", calcular_conflitos(final))

    print("Iteracoes:", iteracoes)
    print("Pioras aceitas:", pioras)

    if calcular_conflitos(final) == 0:
        print("Solucao encontrada!")
    else:
        print("O algoritmo terminou sem encontrar uma solucao.")
