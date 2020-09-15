import random
import pandas as pd
import math
import csv
from numpy import random
import numpy as np

def kmeans(dados,K):
  grupo = []
  centroides = []
  for i in range(K):
    n = random.randint(0,len(dados))
    centroides.append(dados[n])
    grupo.append([dados[n]])

  for k in range(100):
    result = calculaDistancia(centroides,dados,grupo)
    
    novas_centroides = []
    grupo = []

    #novas_centroides(result)
    for i in range(len(result)):
      ponto = []
      for j in range(len(result[i][0])):
        media = 0
        for z in range(len(result[i])):
          media +=result[i][z][j]
        media = np.around(media/(len(result[i])),2)
        ponto.append(media)
      novas_centroides.append(ponto)
      grupo.append([ponto])
    prox = verifica(novas_centroides,centroides)
    if(prox == 0):
      print("Centroides igual")
      return result
    k+1
  return result 
  
def calculaDistancia(X,Y,Grupo):
  for i in range(len(Y)): #Percorrendo dados
    menor = 9999999
    for j in range(len(X)):  #Percorrendo centroides 
        dimensao = len(Y[i])
        dist = distanciaEuclideana(X[j], Y[i], dimensao)
        if(dist < menor): #acha menor
          menor = dist # menor dist de um centroide
          centr = j # Qual centroide corresponde, assim é possivel saber qual o grupo
    Grupo[centr].append(Y[i])

  return Grupo

def distanciaEuclideana(instancia1, instancia2, dimensao):
    distancia = 0
    x=0
    while(x < dimensao):  
      distancia += pow(instancia1[x] - instancia2[x], 2)
      x+=1
    return round(math.sqrt(distancia), 4)

def verifica(X,Y):
  diferenca = 0
  i = 0
  for i in range(len (X)):
    for j in range(len(X[i])):
      if not (X[i][j] == Y[i][j]):
        diferenca +=1
  if diferenca == 0:
    return 0
  else:
    return X

def writeToFile(info, destinyFile):

    with open(destinyFile, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile, delimiter=",")
        for i in info:
            arq.writerow(i)

df = pd.read_csv("/content/sample_data/iris.csv")
X = df.loc[:, df.columns != df.columns[-1]].values
y = df.loc[:, df.columns[-1]].values
K = int(input("Numero de grupos: "))
result = kmeans(X,K)
writeToFile(result, "/content/sample_data/iris2.csv")
for i in result:
  print(i)
