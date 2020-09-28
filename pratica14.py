import pandas as pd
import random
import math
import csv
import numpy as np
import collections

def isNumeric(atributo):
    try:
        float(atributo)
        return True
    except ValueError:
        return False

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

def writeToFile(info, destinyFile):

    with open(destinyFile, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile, delimiter=",")
        for i in info:
            arq.writerow(i)
    print('Arquivo escrito. Verifique.')

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

def evaluatePurity(originFile, arquivodest, K):
    arqEvaluate = associateToCentroids(originFile, K)
    N = 0
    M = 0

    for i in range(len(arqEvaluate) - 1):
        biggest = 0
        tempList = []
        for j in range(len(arqEvaluate[i+1])):

            if (isNumeric(arqEvaluate[i+1][j])):
                num = float(arqEvaluate[i+1][j])
                tempList.append(num)
        
        tempList.sort()
        biggest = tempList[-1]
        N += sum(tempList)
        M += biggest

    purity = M / N 
    #print ("The evaluation of the purity here is: ", purity)
    writeToFile(arqEvaluate, arquivodest)
    return purity

        
## TESTES
print('IMPLEMENTACAO K-MEANS\n')
print("---------------------------------------------------------------------------")
arquivoorig = input('Dataset Original (arquivo.csv): ')
arquivodest = input('Arquivo de Destino (arquivo-destino.txt): ')
K = input('K: ')
print("---------------------------------------------------------------------------")

purity = evaluatePurity(arquivoorig, arquivodest, int(K))
print("THE PURITY OF THIS SHIT IS -->>", purity)

#kMeans = associateToCentroids(arquivoorig, int(K))
# writeToFile(kMeans, arquivodest)