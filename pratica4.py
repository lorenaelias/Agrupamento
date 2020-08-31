import pandas as pd
import math
import csv

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(dimensao):
        distancia += pow(instancia1[x] - instancia2[x], 2)
    return round(math.sqrt(distancia), 4)

def distanciaManhattan(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(dimensao):
        distancia += abs(instancia1[x] - instancia2[x])
    return round(distancia, 4)

def calculaDistancia(X, escolhaDistancia):
    distancias = []
    distancia = []
    for x in range(len(X)):
        for y in range(len(X)):
            dimensao = len(X[x])
            if (escolhaDistancia == '0'):
                dist = distanciaEuclideana(X[x], X[y], dimensao)
            elif (escolhaDistancia == '1'):
                dist = distanciaManhattan(X[x], X[y], dimensao)
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

print("---------------------------------------------------------------------------")
print('Escolha a distancia a ser empregada')
print('0   -       Distancia Euclideana')
print('1   -       Distancia de Manhattan\n')
escolha = input('Escolha:  ')
print("---------------------------------------------------------------------------")
distancias = calculaDistancia(X, escolha)
writeToFile(distancias, arquivodest)