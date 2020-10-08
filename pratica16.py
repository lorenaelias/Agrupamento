import pandas as pd
from numpy.random import RandomState
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris 
from sklearn import metrics # calculo de acurácia
import math

from sklearn.cluster import KMeans

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    for x in range(dimensao):
        distancia += pow(instancia1[x] - instancia2[x], 2)
    return round(math.sqrt(distancia), 4)

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

    #for i in range(len(X)):
    #     group.append((distancias[i].index(min(distancias[i]))))

    return distancias

def silhueta_simplificada(dados):
  somatorio = 0 
  for i in range(len(dados)):
    somatorio += sil(dados[i],cluster[i])
    print(sil(dados[i],cluster[i]))

  silhueta = somatorio/len(dados)

  if(silhueta > 0): return ("bom")
  else: return ("ruim")

def sil(obj,clusterPertencente):
  distanciaObjetoAtéClusterProximo = 9999999999
  for i in range(len(centroides)):
    if not (i == clusterPertencente):
      dist = distanciaEuclideana(obj,centroides[i],5)
      if dist < distanciaObjetoAtéClusterProximo:
        distanciaObjetoAtéClusterProximo = dist
  
  distanciaObjetoAtéCentroide = distanciaEuclideana(obj,centroides[clusterPertencente],4)
  si = distanciaObjetoAtéClusterProximo - distanciaObjetoAtéCentroide
  if (distanciaObjetoAtéClusterProximo > distanciaObjetoAtéCentroide):
    si = si/distanciaObjetoAtéClusterProximo
  else:  
    si = si/ distanciaObjetoAtéCentroide
  print(si)
  return si

if __name__ == "__main__":
  df = pd.read_csv('datasets/iris.csv')

  X = df.loc[:,df.columns != "variety"].values

  print(X)

  kmeans = KMeans(n_clusters= 2, random_state=0).fit(X)

  cluster = kmeans.labels_
  print(cluster)

  centroides = kmeans.cluster_centers_
  for i in centroides:
    print(i)

  x = calculaDistancia(X,X)
  for i in x:
    print(i)

  result = silhueta_simplificada(X)
  print(result)