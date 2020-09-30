import pandas as pd
import random
import math
import csv
import collections
import numpy as np
import os

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(dimensao):
        distancia += pow(float(instancia1[x]) - float(instancia2[x]), 2)
    return round(math.sqrt(distancia), 2)

def randomCentroids(X, K):
    randomList = []

    for i in range (K):
        n = random.randint(0, len(X) - 1)
        randomList.append(X[n])

    return randomList

def calculaDistancia(X, centroids):
    distancias = []
    distancia = []
    group = []

    for x in range(len(X)):
        for y in range(len(centroids)):
            dimensao = len(X[x])
            dist = distanciaEuclideana(X[x], centroids[y], dimensao)            
            distancia.append(dist)
        distancias.append(distancia)
        distancia = []

    for i in range(len(X)):
         group.append((distancias[i].index(min(distancias[i]))))

    return group

def getNewCentroids(X, group, K):
    groupQuantity = []
    newCentroids = []
    sumList = []
    listOfZeros = [0] * len(X[0])

    for k in range(K):
        groupQuantity.append(0)
        newCentroids.append(listOfZeros)

    for k in range(K):
        for i in range(len(X)):
            if group[i] == k:
                groupQuantity[k] += 1
                newCentroids[k] = [float(a) + float(b) for a, b in zip(newCentroids[k], X[i])]
        if groupQuantity[k] != 0:
            newCentroids[k] = [float(a) / groupQuantity[k] for a in newCentroids[k]]

    roundedNewCentroids = np.around(newCentroids, 2)

    return roundedNewCentroids

def associateToCentroids(originFile, K):
    dataFrame = pd.read_csv(originFile, encoding = "UTF-8", sep = ",", header = None)
    X = dataFrame.loc[:, dataFrame.columns != dataFrame.columns[-1]].values
    X = X[1:]
    arq = open(originFile, 'r')
    lines = arq.readlines()
    arq.close()
    arqFinal = []

    for line in lines: 
        arqFinal.append(line.strip().split(","))
     
    centroids = randomCentroids(X, K)
    gruposDistancias = calculaDistancia(X, centroids)

    centrBool = [True] * K
    areAllEqual = False

    for i in range(100):
        oldCentroids = centroids
        centroids = getNewCentroids(X, gruposDistancias, K)
        gruposDistancias = calculaDistancia(X, centroids)
        for k in range(K):
            if oldCentroids[k] in centroids:
                centrBool[k] = True
            else:
                centrBool[k] = False
        areAllEqual = all(elem == centrBool[0] for elem in centrBool)
        if centrBool[0] == True & areAllEqual == True:
            break
    
    arqFinal[0].append("cluster")
    for z in range(len(X)):
        lastIndex = len(X[z]) - 1
        arqFinal[z+1].append(gruposDistancias[z])

    return arqFinal

def generateConfusionMatrix(originFile, K):
    arqEvaluate = associateToCentroids(originFile, K)
    classPos = len(arqEvaluate[1]) - 2                  ## posição da classe em cada objeto
    clusterPos = len(arqEvaluate[1]) - 1                ## posição da designação de clusters após o K-Means
    classes = []

    for i in range(len(arqEvaluate) - 1):
        classes.append(arqEvaluate[i+1][classPos])

    classes = list(set(classes))
    confusionMatrix = [[0 for j in range(len(classes))] for i in range(K)]     ## inicializei a matriz de confusão com as linhas e colunas vazias

    for i in range(len(arqEvaluate) - 1):

        for k in range(K):

            if (arqEvaluate[i+1][clusterPos] == k): 
                for j in range(len(classes)):
                    if (arqEvaluate[i+1][classPos] == classes[j]):
                        confusionMatrix[k][j] += 1
    
    return confusionMatrix

def evaluatePurity(originFile, arquivodest, K):
    confusionMatrix = generateConfusionMatrix(originFile, K)
    N = 0
    M = 0

    print(f"\n----Aqui está nossa matriz de confusão para K = {K}----\n")
    for i in confusionMatrix:
        print(i)

    for i in range(len(confusionMatrix)):
        N += sum(confusionMatrix[i])
        M += max(confusionMatrix[i])

    purity = M / N
    response = f"Pureza com K = {K}: {purity}\n"

    writeToFile(response, arquivodest)

def writeToFile(info, arquivodest):

    if os.path.exists(arquivodest):
        mtdEscrita = 'a' # append if already exists
    else:
        mtdEscrita = 'w' # make a new file if not

    arq = open(arquivodest, mtdEscrita)

    arq.write(info)
    arq.close()
            
## TESTES
print('\nANÁLISE DE PUREZA DE UM CLUSTER K-MEANS PARA -->> K = 2  K = 3   K = 4\n')
print("---------------------------------------------------------------------------")
arquivoorig = input('Dataset Original (arquivo.csv): ')
arquivodest = input('Arquivo de Destino (arquivo-destino.txt): ')
print("---------------------------------------------------------------------------\n")

evaluatePurity(arquivoorig, arquivodest, 2)
evaluatePurity(arquivoorig, arquivodest, 3)
evaluatePurity(arquivoorig, arquivodest, 4)
