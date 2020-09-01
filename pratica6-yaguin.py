import pandas as pd
import random
import math
import csv
import numpy as np
import collections

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(int(dimensao)):
        distancia += pow(float(instancia1[x]) - float(instancia2[x]), 2)
    return round(math.sqrt(distancia), 2)

def randomCentroids(X, K):
    randomList = []
    # X = np.array(dataFrame)
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

# Group aqui é a lista que contém os 0, 1, 2, ou seja, a lista de grupos para que eu possa usar seus index na soma
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

def writeToFile(info, destinyFile):

    with open(destinyFile, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile, delimiter=",")
        for i in info:
            arq.writerow(i)

def associateToCentroids(originFile, K):
    dataFrame = pd.read_csv(originFile, encoding = "UTF-8", sep = ",", header = None)
    # X = np.array(dataFrame)
    X = dataFrame.loc[:, dataFrame.columns != dataFrame.columns[-1]].values   #tirei a ultima coluna, a gente n usa (classe)
    X = X[1:]   #tirei a primeira linha (header), só atrapalha
    print(X)
    arq = open(originFile, 'r')
    lines = arq.readlines()
    arq.close()
    arqFinal = []

    for line in lines: 
        arqFinal.append(line.strip().split(","))
     
    # Centroides randomicos e as distancias destes com o resto dos objetos
    centroids = randomCentroids(X, K)
    gruposDistancias = calculaDistancia(X, centroids)

    # Por enquanto, 50 iterações é o limite
    for i in range(50):
        oldCentroids = centroids
        centroids = getNewCentroids(X, gruposDistancias, K)
        gruposDistancias = calculaDistancia(X, centroids)
        if np.all( oldCentroids == centroids):  # Se os centroides se mantiverem iguais, então nossa iteração chega ao fim
            break
    
    for z in range(len(X)):
        lastIndex = len(X[z]) - 1
        arqFinal[z+1].append(gruposDistancias[z])
    return arqFinal

        
## TESTES

kMeans = associateToCentroids("datasets/iris.csv", 3)
writeToFile(kMeans, "datasets/iris2.csv")