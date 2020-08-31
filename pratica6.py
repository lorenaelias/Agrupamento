import random
import pandas as pd
import math
import csv
from numpy import random

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

def kmeans(X):
  centroides = []
  for i in range(5):
    n = random.randint(0,len(X))
    centroides.append(X[n])
  print(centroides)
  #while():
   # for i in X:
    #  dist = calculaDistancia(i,centroides, )

df = pd.read_csv("/content/sample_data/iris.csv")
X = df.loc[:, df.columns != df.columns[-1]].values
y = df.loc[:, df.columns[-1]].values
print(len(X))
result = kmeans(X)

