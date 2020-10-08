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
        distancia += pow(instancia1[x] - instancia2[x], dimensao)
    return round(math.sqrt(distancia), 4)

def calculaDistancia(X, centroids):
    distancias = []
    distancia = []

    for x in range(len(X)):
        for y in range(len(centroids)):
            dist = distanciaEuclideana(X[x], centroids[y], len(X[x]))            
            distancia.append(dist)
        distancias.append(distancia)
        distancia = []

    return distancias

def silhueta_simplificada(dados,cluster,centroides):
  somatorio = 0 
  for i in range(len(dados)):
    somatorio += sil(dados[i],cluster[i],centroides)
    print(sil(dados[i],cluster[i],centroides))

  silhueta = somatorio/len(dados)

  if(silhueta > 0): return ("bom")
  else: return ("ruim")

def sil(obj,clusterPertencente,centroides):
  distanciaObjetoAtéClusterProximo = 9999999999
  for i in range(len(centroides)):
    if not (i == clusterPertencente):
      dist = distanciaEuclideana(obj,centroides[i],len(obj))
      if (dist < distanciaObjetoAtéClusterProximo):
        distanciaObjetoAtéClusterProximo = dist
  
  distanciaObjetoAtéCentroide = distanciaEuclideana(obj,centroides[clusterPertencente],len(obj))
  si = distanciaObjetoAtéClusterProximo - distanciaObjetoAtéCentroide
  if (distanciaObjetoAtéClusterProximo > distanciaObjetoAtéCentroide):
    si = si/distanciaObjetoAtéClusterProximo
  else:  
    si = si/ distanciaObjetoAtéCentroide
  return si

def main():
    df = pd.read_csv('iris.data')
    print(df.head())
    X = df.loc[:,df.columns != "Iris-setosa"].values
    print(X)
    kmeans = KMeans(n_clusters= 3, random_state=0).fit(X)
    centroides = kmeans.cluster_centers_
    for i in centroides:
        print(i)
    cluster = kmeans.labels_
    print(cluster)
    result = silhueta_simplificada(X,cluster,centroides)
    print(result)