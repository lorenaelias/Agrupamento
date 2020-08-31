import csv

def isNumeric(atributo):
    try:
        float(atributo)
        return True
    except ValueError:
        return False

def findMedia(numeros):
    total = 0.0
    size = 0

    for i in numeros:
        if (isNumeric(i)):
            size += 1
            total += float(i)

    total /= size
    return str(total)

def findModa(info):
    maximum = 0
    realMaximum = 0
    moda = ""

    for inf in info:
        for i in info:
            if inf == i:
                maximum += 1
                
        if (maximum > realMaximum):
            realMaximum = maximum
            moda = inf
        
        maximum = 0
    
    return moda

def getHeader(fileName, delimiter):
    arq = open(fileName, 'r')
    header = arq.readline()
    arq.close()
    return header.strip().split(delimiter)

def readEstimateCorrect(fileName, delimiter, emptySpace):

    arq = open(fileName, 'r')
    header = arq.readline()
    lines = arq.readlines()
    arq.close()
    objAnalise = []
    quickArray =[]

    for line in lines: 
        objAnalise.append(line.strip().split(delimiter))

    for j in range(len(objAnalise)-1): 
        for k in range(len(objAnalise[j])):

            if (objAnalise[j][k] == emptySpace):
                for x in range(len(objAnalise)):
                    quickArray.append(objAnalise[x][k])

                if (j == 0):

                    for l in range(len(objAnalise)):

                        if (objAnalise[j + l][k] != emptySpace):

                            if (isNumeric(objAnalise[j + l][k])):
                                objAnalise[j][k] =  findMedia(quickArray) 
                            else:
                                objAnalise[j][k] =  findModa(quickArray)  
                            
                            break

                else:

                    for l in range(len(objAnalise)):

                        if (objAnalise[j - l][k] != emptySpace):

                            if (isNumeric(objAnalise[j - l][k])):
                                objAnalise[j][k] = findMedia(quickArray) 
                            else:
                                objAnalise[j][k] = findModa(quickArray)  

                            break
        quickArray = []
    return objAnalise


def writeToFile(info, fileName, dataset, delimiter):

    with open(fileName, 'w', newline='') as csvfile:
        arq = csv.writer(csvfile)
        arq.writerow(getHeader(dataset, delimiter))
        for i in info:
            arq.writerow(i)
            
    print("Valores faltantes corrigidos")

def visualize(data):
    for i in data:
        print(i,'\n')

def main():
    print('\n--------------------------------------------------')
    dataset = input('Dataset Original (dataset.csv): ')
    destino = input('Dataset de Destino (dataset-destino.csv): ')

    print('\n--------------------------------------------------')
    print("\nDelimitador:")
    print('Para usar ","           digite 0')
    print('Para usar ";"           digite 1')
    print('Para usar outro         digite 2\n')
    escolha = input("Escolha:   ")

    if(escolha == '0'):
        delimitador = ","
    elif(escolha == '1'):
        delimitador = ";"
    elif(escolha == '2'):
        print('')
        delimitador = input("Delimitador desejado:   ")
    else:
        print('')
        print('Valor inexistente')
        exit()

    print('\n--------------------------------------------------')
    print("\nSimbolo de valor faltante:")
    print('Para usar ""             digite 0')
    print('Para usar "?"            digite 1')
    print('Para usar " ?"           digite 2')
    print('Para usar outro          digite 3\n')
    escolha = input("Escolha:   ")

    if(escolha == '0'):
        valoresFaltantes = ""
    elif(escolha == '1'):
        valoresFaltantes = "?"
    elif(escolha == '2'):
        valoresFaltantes = " ?"
    elif(escolha == '3'):
        print('')
        valoresFaltantes = input("Simbolo de valor faltante desejado:   ")
    else:
        print('')
        print('Valor inexistente')
        exit()

    print('\n--------------------------------------------------')
    
    arquivo = readEstimateCorrect(dataset, delimitador, valoresFaltantes)
    writeToFile(arquivo, destino, dataset, delimitador)

main()