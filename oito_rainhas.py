import random


def mostrar_tabuleiro(tabuleiro):
    tamanho = len(tabuleiro) 
    """ tamanho da lista """    
        
    for linha in range(tamanho):
        for coluna in range(tamanho):
            """A rainha desta coluna está na linha que estamos desenhando agora?"""
            if tabuleiro[coluna] == linha:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

def criar_tabuleiro(tamanho=8):
    tabuleiro = []

    for coluna in range(tamanho):
        linha_aleatoria = random.randrange(tamanho)

        tabuleiro.append(linha_aleatoria) #coloca a linha sorteada no final da lista
    return tabuleiro

def calcular_conflitos(tabuleiro):
    tamanho = len(tabuleiro)
    conflito = 0

    for coluna1 in range(tamanho):
        for coluna2 in range(coluna1 + 1, tamanho):
            
            mesmalinha = (
                tabuleiro[coluna1] == tabuleiro[coluna2]
            )

            distancia_colunas = abs(coluna1 - coluna2)
            
            distancia_linhas = abs(tabuleiro[coluna1] - tabuleiro[coluna2])

            mesma_diagonal = distancia_colunas == distancia_linhas

            if mesmalinha or mesma_diagonal:
                conflito += 1

    return conflito

if __name__ == "__main__":
    
    tabuleiro = criar_tabuleiro()

    print(tabuleiro)

    mostrar_tabuleiro(tabuleiro)

    resultado = calcular_conflitos(tabuleiro)

    print("Conflitos:", resultado)

