import random
import math

from oito_rainhas import criar_tabuleiro
from oito_rainhas import mostrar_tabuleiro
from oito_rainhas import calcular_conflitos

def gerar_vizinho(tabuleiro):
    vizinho = tabuleiro.copy()

    coluna = random.randrange(len(tabuleiro))

    linha_atual = vizinho[coluna]

    nova_linha = random.randrange(len(tabuleiro))

    while nova_linha == linha_atual:
        nova_linha = random.randrange(len(tabuleiro))
    
    vizinho[coluna] = nova_linha 

    return vizinho

if __name__ == "__main__":
    atual = criar_tabuleiro()
    vizinho = gerar_vizinho(atual)
    #problema antes do movimento
    conflitos_atual = calcular_conflitos(atual)
    #problema depois do movimento
    conflitos_vizinho = calcular_conflitos(vizinho)

    print("Atual:", atual)
    print("Conflitos do atual:", conflitos_atual)

    print("Vizinho:", vizinho)
    print("Conflitos do vizinho:", conflitos_vizinho)

    delta = conflitos_vizinho - conflitos_atual

    if delta < 0:
        print("O vizinho é melhor")

    elif delta == 0:
        print("O vizinho tem a mesma quantidade de conflitos")

    else:
        print("O vizinho é pior")


        