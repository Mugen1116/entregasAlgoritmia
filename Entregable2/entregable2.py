'''
Created on 1 nov. 2017
@author:    Group 7.
            Sergio Landete
            Luis Miguel Agudo
            Ben Schepmans

EI1022 Algoritmia 2017/2018 
'''
from sys import argv

'''
================================================================================
//
//    $python3 entregable2 <cadena de caras y cruces>
//
================================================================================

'''
import sys

def giraMonedas ( cadena, n ):
    cadenaDevolver = ""
    for i in range(0, n):
        letra = cadena[i]
        if letra == 'o': #Cara
            cadenaDevolver += str('x')
        else: #cruz
            cadenaDevolver += str('o') 
    
    #Revertir el trozo que hemos girado y concatenamos el resto de cadena
    return cadenaDevolver[::-1] + cadena[n::1]
   


def algoritmo ( pila: "Sting desordenado" ) -> "String ordenado":
    
    def subalgoritmo (): #Recibe las monedas en el momento actual y devolverá numero de monedas a girar o -1 si está todo hacia arriba
        contador = 0
        empezado = pila[0]
        for letra in pila:
            if empezado == letra:
                contador += 1
            else:
                break
        #Comprobar si todo está boca arriba
        if  contador == len(pila) and empezado == 'o':
            return -1
        else:
            return contador
    
    terminar = False
    devolver =[]
    #Iniciamos un contador a 0
    #Vamos a contar el número de monedas hasta encontrar la primera cara
    while ( not terminar ):
        variable = subalgoritmo()
        pila = giraMonedas(pila,variable)
        if variable == -1:
            terminar = True
        else:
            devolver.append(variable)
        
    #Deverá girar
    return devolver

def main( args: 'String[]' ):
    
    if len (argv) != 2:
        print ("Error: Wrong Arguments: use: $python3 entregable2.py 'Cadena' ")
    else:
        lista = algoritmo(argv[1])
        for num in lista:
            print(num) 

if __name__ == '__main__':
    main( sys.argv[1:] )