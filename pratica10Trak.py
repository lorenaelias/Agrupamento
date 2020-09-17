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
        for y in range(x):
            if( y == x ):
                break
            dimensao = len(X[x])
            dist = distanciaEuclideana(X[x], X[y], dimensao)
            distancia.append(dist)
        distancias.append(distancia)
        distancia = []
    return distancias

def SingleLink(L):
    menor = 99999999999
    pos_x = 0
    pos_y = 0
    nx = 0
    ny = 0
    #Achar o minimo
    for x in range(1,len(L)):
        for y in range(x):
            if L[x][y] < menor and L[x][y] != (-1):
                pos_x = x
                pos_y = y
                menor = L[x][y]
    
    #Novas posições da antiga matriz
    Novas_pos = [[]]
    for i in range(len(L)):
        if i == pos_x or i == pos_y:
            if pos_x < pos_y:
                Novas_pos[0].append(i)
            else:
                Novas_pos[0].append(i)
        else: 
            Novas_pos.append(i)
    #Fazer nova matriz
    Nova_matriz = []

    for i in range(len(Novas_pos)):
        Nova_matriz.append([-1] *(i+1))

    print(len(L))
    for x in range(0,((len(L)))):
        for y in range(0,len(L[x])):
            if(((x == pos_x or x == pos_y) and (y == pos_x or y == pos_y)) or x == y):
                continue
            #Achar nova posicao na nova matriz
            if( x == pos_x or x == pos_y):
                nx = 0
            if( y == pos_y or y == pos_x):
                ny = 0

            for a in range(1,len(Novas_pos)):
                if x == Novas_pos[a]:
                    nx = a
                if y == Novas_pos[a]:
                    ny = a

            #Fazer a nova matriz
            if(nx != 0):
                if(Nova_matriz[nx][ny] == -1):
                    Nova_matriz[nx][ny] = L[x][y]
                else: 
                    if(Nova_matriz[nx][ny] > L[x][y]):
                        Nova_matriz[nx][ny] = L[x][y]
            else:
                if(Nova_matriz[ny][nx] == -1):
                    Nova_matriz[ny][nx] = L[x][y]
                else: 
                    if(Nova_matriz[ny][nx] > L[x][y]):
                        Nova_matriz[ny][nx] = L[x][y]

    for i in Nova_matriz:
        i.pop()
    return Nova_matriz
    

def writeToFile(info, fileName):
    with open(fileName, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile)
        for i in info:
            arq.writerow(i)
    print("Arquivo escrito.")
        
#print("---------------------------------------------------------------------------")
#arquivoorig = input('Dataset Original (arquivo.csv): ')
arquivodest = input('Arquivo de Destino (arquivo-destino.txt): ')
print("---------------------------------------------------------------------------")
#df = pd.read_csv(arquivoorig)

#X = df.loc[:, df.columns != df.columns[-1]].values
#y = df.loc[:, df.columns[-1]].values

distancias = [[],[2],[6,5],[10,8,4],[9,8,5,3]]
final = []
final.append(distancias)
#distancias = calculaDistancia(X)
result = SingleLink(distancias)
final.append(result)
#writeToFile(result, arquivodest)

while (len(result) > 2 ):
    result = SingleLink(result)
    final.append(result)
#print(final)
writeToFile(final, arquivodest)
