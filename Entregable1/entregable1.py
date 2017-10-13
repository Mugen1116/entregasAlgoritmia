'''
Created on 4 oct. 2017
@author:    Group 7.
            Sergio Landete
            Luis Miguel Agudo
            Ben Schepmans

EI1022 Algoritmia 2017/2018 
'''
import sys
from algoritmia.datastructures.digraphs import UndirectedGraph
from labyrinthviewer import LabyrinthViewer
from algoritmia.datastructures.queues import Fifo

'''
================================================================================
//
//    $python3 entregable1 <fichero_laberinto.i> Optional <-g> ->Show labyrinth
//
================================================================================

'''

#Recibe fichero(laberinto) devuelve UndirectedGraph
def load_labyrinth( file: 'TextIOWrapper') -> ('UndirectedGraph'): 
    #Funcion auxiliar para ver los vecinos donde se encuentran
    def get_vecino(v: ('int', 'int'), pasillo: 'String') -> ('int', 'int'):
    # Dado un punto y un pasillo (Arista) , obtiene la casilla adyacente
        f, c = v
        if pasillo == "n":
            return f - 1, c
        if pasillo == "s":
            return f + 1, c
        if pasillo == "e":
            return f, c + 1
        #Si no es norte, ni sur ni es, solo puede ser oeste
        return f, c - 1
    # END get_vecino
    matriz_laberinto = []
    for i, line in enumerate(file):
        line = line.split('\n')
        matriz_laberinto.append([])
        for v in line[0].split(','):
            matriz_laberinto[i].append(v)

    laberinto = []
    for f, fila in enumerate(matriz_laberinto):
        for c, v in enumerate(fila):
            todas_paredes = {"n", "s", "e", "w"}
            paredes = set(v[:])
            pasillos = todas_paredes - paredes
            for pasillo in pasillos:
                laberinto.append(((f, c), get_vecino((f, c), pasillo)))
    return UndirectedGraph(E=laberinto)
# FIN load_labyrinth

'''
FUNCIONES AUXILIARES DE RECORRIDO
'''
#Recorrido en anchura
def recorre_anchura(grafo, v_inicial):
        aristas = []
        queue = Fifo()
        seen = set()
        queue.push( (v_inicial, v_inicial) )
        distancia = {}
        seen.add(v_inicial)
        while len(queue) > 0:
            u, v = queue.pop()
            distancia[v_inicial] = 0
            aristas.append( (u,v) )
            for suc in grafo.succs(v):
                if suc not in seen:
                    '''
                    AÑADIDO: Diccionario con las distancias hasta cada vértice desde el vértice inicial
                    '''
                    #Si no es un sucesor, ahora si, entonces se incrementa la distancia en uno
                    distancia[suc] = distancia[v] +1 
                    seen.add(suc)
                    queue.push((v,suc))
        
        return aristas, distancia
#END Recorrido en anchura
#========================================
#Recuperador de camino
def recuperador_camino(lista, v):
    bp = {}
    for o,d in lista:
        bp[d] = o
    camino = []
    camino.append(v)
    while v != bp[v]:
        camino.append(v)
        v = bp[v]
    camino.append(v) #Para añadir el primer elemento
    camino.reverse()
    return camino
#END recuperador

#Funcion paracalcular distancia más lejana desde un v_inicial
def calcula_distancias ( distancia ):    
    for habita, dist in distancia.items():
        vert = habita
        pasos = dist
    return vert, pasos
#END calcula_distancia

 

'''
END FUNCIONES AUXILIARES DE RECORRIDO
'''


'''
=================== MAIN ======================
'''
def main( args: 'String[]' ):
    if  len(args) < 1 or len(args) > 2:
        print("Error de argumentos \nUso: python3 entregable1.py <laberinto> <-g>(Opcional)->Mostrar laberinto")        
    #elif args[1] != "-g":
    #        print("Error de argumentos \nUso: python3 entregable1.py <laberinto> <-g>(Opcional)->Mostrar laberinto")
    else:
        show_labyrinth = False
        if len(args) == 2 and args[1] == "-g":
            show_labyrinth = True
        
        file = open( args[0], 'r' )
        laberinto = load_labyrinth(file)
        
        #Utilizando el 0,0 comenzamos a buscar el camino más largo desde este punto
        u_inicial = (0,0)
        camino1, distancia1 = recorre_anchura(laberinto, u_inicial)
        posibleV, pasos1 = calcula_distancias(distancia1)
        #Tenemos el punto más lejano desde (0,0)
        #Utilizando este punto, volvemos a buscar el más lejano a este nuevo
        camino2, distancia2 = recorre_anchura(laberinto, posibleV)
        posibleU, pasos2 = calcula_distancias(distancia2)
        
        #Ahora con los tres posibles puntos
        #Resolver empates        
        u = u_inicial
        #Resolver el empate de U
        if pasos2 == pasos1:
            if (posibleU[0] < u_inicial[0] ) or ( posibleU[0] == u_inicial[0] and posibleU[1] < u_inicial[1] ):
                u = posibleU
        elif pasos2 > pasos1:
            u = posibleU
        #Resolver condicion con u y u
        
        if  posibleV[0] < u[0] or (  posibleV[0] == u[0] and  posibleV[1] < u[1] ):
            v = u
            u = posibleV
        else:
            v = posibleV
        
        #Show solution
        print( u[0] , u[1]) #Punto inicio
        print( v[0], v[1]) #Punto llegada
        print( pasos1 if pasos1 > pasos2 else pasos2 ) #Distancia
        
        if show_labyrinth:
            if u == u_inicial:
                lista = camino1
                caminoImprimir = recuperador_camino(lista, v)
            else:
                lista = camino2
                caminoImprimir = recuperador_camino(lista, u)
            lv = LabyrinthViewer(laberinto, 760, 480)
            lv.add_path(caminoImprimir, 'red')
            lv.run()    
#End main    
#Run main
if __name__ == '__main__':
    main( sys.argv[1:] )
