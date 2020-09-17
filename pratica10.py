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

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(dimensao):
        distancia += pow(instancia1[x] - instancia2[x], 2)
    return round(math.sqrt(distancia), 4)

def calculaDistancia(X):
    distancias = []
    distancia = []
    for x in range(len(X)):
        for y in range(len(X)):
            dimensao = len(X[x])
            dist = distanciaEuclideana(X[x], X[y], dimensao)
            distancia.append(dist)
        distancias.append(distancia)
        distancia = []
    return distancias

def writeToFile(info, fileName):
    with open(fileName, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile)
        for i in info:
            arq.writerow(i)
    print("Arquivo escrito.")
    
print("---------------------------------------------------------------------------")
arquivoorig = input('Dataset Original (arquivo.csv): ')
arquivodest = input('Arquivo de Destino (arquivo-destino.txt): ')
print("---------------------------------------------------------------------------")
df = pd.read_csv(arquivoorig)

X = df.loc[:, df.columns != df.columns[-1]].values
y = df.loc[:, df.columns[-1]].values

distancias = calculaDistancia(X)
writeToFile(distancias, arquivodest)