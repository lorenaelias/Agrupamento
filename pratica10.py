#IMPLEMENTACAO SINGLE LINK
#medida de dist: euclideana
#condicao de parada: um unico grupo seja obtido

#remover classe da base de dados (ultima coluna)

#entrada: arquivo .csv
#saida: 
        #uma abordagem possivel:
        # arquivo indicando em cada nivel de hierarquia qual par de elementos foi unido,
        # o nivel é representado pela posicao no arquivo. Cada linha deve corresponder a um nivel.

        #outra abordagem possivel:
        # indicar em cada nivel de hieraquia qual foi o resultado do agrupamento. Cada linha do arquivo
        # indica um nivel da hierarquia. Os grupos são separados por virgula, sendo cada grupo
        # representado por {} e seus elementos separados por virgula também.

import pandas as pd
import math
import csv
import ast

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(dimensao):
        distancia += pow(instancia1[x] - instancia2[x], 2)
    return round(math.sqrt(distancia), 4)

def calculaDistancia(X):
    #retorna a matriz de distancias (somente a parte triangular inferior)
    distancias = []
    distancia = []
    for x in range(len(X)):
        for y in range(len(X)):
            if(x == y):
                break
            dimensao = len(X[x])
            dist = distanciaEuclideana(X[x], X[y], dimensao)
            distancia.append(dist)
        distancias.append(distancia)
        distancia = []
    return distancias

def minDistancia(distancias):
    #retorna a posicao da menor distancia na matriz distancias

    # print ("zero:", distancias[1])
    minus = distancias[1][0]
    pos = [1, 0]
    
    for i in range(2, len(distancias)):
        aux = distancias[i].index(min(distancias[i]))
        # print(aux)
        if(distancias[i][aux] < minus):
            minus = distancias[i][aux]
            pos = [i, aux]
    # print(distancias[pos[0]][pos[1]])
    # print(pos)
    return pos

def mergeLinhas(distancias, pos):
    # - distancias é a matriz de distancias
    # - pos é uma lista de dois elementos que contem a posicao dos objetos 
    #   que possuem menor distancia entre si
    # 
    # retorna a matriz de distancias depois de fundir as linhas e colunas
    # dos objetos que estao nas posicoes pos

    novaLinha = []
    if(pos[0] > pos[1]):
        aux = pos[0]
        pos[0] = pos[1]
        pos[1] = aux

    for i in range(len(distancias[pos[0]])):
        if( pos[0] == i ):
            min = distancias[i][pos[0]]
            pos = [i, pos[0]]
            continue
        else:
            min = distancias[pos[0]][i]
        if( pos[1] == i ):
            continue
        if( distancias[pos[1]][i] < distancias[pos[0]][i] ):
            min = distancias[pos[1]][i]
            pos = [pos[1], i]
        novaLinha.append(min)
    if( len(novaLinha) == 0 ):
        novaPosLinha = 0
    elif( novaLinha[-1] == 0 ):
        novaLinha = novaLinha[:-2]
    else:
        novaPosLinha = len(novaLinha)

    # print(novaLinha, novaPosLinha)

    #calcular novaColuna
    novaColuna = []
    valorPos0 = 0
    valorPos1 = 0
    for i in range(len(distancias)):
        if(len(distancias[i]) > pos[0]):
            # print('pos0')
            # print(distancias[i][pos[0]])
            valorPos0 = distancias[i][pos[0]]
            
        if(len(distancias[i]) > pos[1]):
            # print('pos1')
            # print(distancias[i][pos[1]])
            valorPos1 = distancias[i][pos[1]]

        if(valorPos1 < valorPos0):
            minColuna = valorPos1
        else:
            minColuna = valorPos0
        novaColuna.append(minColuna)
    
    # print(novaColuna)

    #deletar as linhas e colunas pos[0] pos[1]
    
    for i in range(len(distancias)):
        if(len(distancias[i]) > pos[1]):
            # print(pos[1])
            # print(distancias[i])
            # print(len(distancias[i]))
            del distancias[i][pos[1]]
    
    for i in range(len(distancias)):
        if(len(distancias[i]) > pos[0]):
            del distancias[i][pos[0]]

    del distancias[pos[1]]
    del distancias[pos[0]]

    #inserir linha na novaPosLinha a novaLinha
    distancias.insert(novaPosLinha, novaLinha)

    del novaColuna[0]

    for i in range(len(distancias)):
        distancias[i].insert(novaPosLinha, novaColuna[i])

    #inserir coluna novaColuna na posicao novaPosLinha
    # print(distancias)

    for i in range(len(distancias)):
        if distancias[i][-1] == 0:
            del distancias[i][-1]

    # print(distancias)

    return distancias

def iterarMatriz(distancias):
    #parada quando tivermos matriz 2x2 ( len(distancias) == 2 )
    tamanho = len(distancias)
    if(tamanho <= 2):
        raise Exception("Tamanho nao suportado")

    distanciasEscrita = []
    distanciasEscrita.append(str(distancias))
    print(distanciasEscrita)

    while(tamanho != 2):
        posMin = minDistancia(distancias)
        novasDistancias = []
        novasDistancias = mergeLinhas(distancias, posMin)
        # print(novasDistancias)
        distanciasEscrita.append(str(novasDistancias)) 
        
        tamanho = tamanho - 1

    # TODO: problema - distancias e novasDistancias sao tratados como objetos
    #         e objetos em python sao tratados como ponteiros
    #       fiz um casting pra str, mas ai da problema na hora de gravar no arquivo
    print(distanciasEscrita)
    writeToFile(distanciasEscrita, "hierarquia.txt")

def writeToFile(info, fileName):
    with open(fileName, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile)
        for i in info:
            res = ast.literal_eval(i) 
            
            arq.writerow(res)
    print("Arquivo escrito.")
    
if __name__ == "__main__":
    # print("---------------------------------------------------------------------------")
    # arquivoorig = input('Dataset Original (arquivo.csv): ')
    # arquivodest = input('Arquivo de Destino (arquivo-destino.txt): ')
    # print("---------------------------------------------------------------------------")
    # df = pd.read_csv(arquivoorig)

    df = pd.read_csv("datasets/iris.csv")
    arquivodest = "hierarquia.txt"
    X = df.loc[:, df.columns != df.columns[-1]].values
    y = df.loc[:, df.columns[-1]].values

    distancias = calculaDistancia(X)

    #teste do exercicio1 pratica9
    distancias = [    
    [],
    [2],		
    [6, 5],	
    [10, 8, 4],
    [9, 8, 5, 3]
    ]

    # distancias = [    
    # [],		
    # [5],	
    # [8, 4],
    # [8, 5, 3]
    # ]

    # distancias = [    
    # [],		
    # [5],	
    # [8, 4]
    # ]

    # distancias = [    
    # [],		
    # [5]
    # ]

    #exemplo da indiana 1
    # distancias = [
    #     [],
    #     [23],
    #     [22, 15],
    #     [37, 20, 15],
    #     [34, 14, 28, 29],
    #     [23, 25, 11, 22, 39]
    # ]
    
    iterarMatriz(distancias)