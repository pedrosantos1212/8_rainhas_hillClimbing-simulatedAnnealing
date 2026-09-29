import random


def mostrar_tabuleiro(tabuleiro):
    # A quantidade de elementos define as linhas e colunas.
    tamanho = len(tabuleiro)

    # Desenha uma linha por vez.
    for linha in range(tamanho):
        for coluna in range(tamanho):
            # O indice e a coluna; o valor guardado e a linha.
            if tabuleiro[coluna] == linha:
                print("Q", end=" ")
            else:
                print(".", end=" ")

        # Pula para a proxima linha do desenho.
        print()


def criar_tabuleiro(tamanho=8):
    tabuleiro = []

    # Coloca uma rainha em uma linha aleatoria de cada coluna.
    for coluna in range(tamanho):
        linha_aleatoria = random.randrange(tamanho)
        tabuleiro.append(linha_aleatoria)

    return tabuleiro


def calcular_conflitos(tabuleiro):
    tamanho = len(tabuleiro)
    conflito = 0

    # Compara cada rainha apenas com as rainhas seguintes.
    for coluna1 in range(tamanho):
        for coluna2 in range(coluna1 + 1, tamanho):
            # Valores iguais significam rainhas na mesma linha.
            mesma_linha = tabuleiro[coluna1] == tabuleiro[coluna2]

            # Distancias iguais indicam uma diagonal.
            distancia_colunas = abs(coluna1 - coluna2)
            distancia_linhas = abs(tabuleiro[coluna1] - tabuleiro[coluna2])
            mesma_diagonal = distancia_colunas == distancia_linhas

            # Cada par que se ataca soma um conflito.
            if mesma_linha or mesma_diagonal:
                conflito += 1

    return conflito


if __name__ == "__main__":
    # Teste executado apenas quando este arquivo e aberto diretamente.
    tabuleiro = criar_tabuleiro()

    print(tabuleiro)
    mostrar_tabuleiro(tabuleiro)

    resultado = calcular_conflitos(tabuleiro)
    print("Conflitos:", resultado)
