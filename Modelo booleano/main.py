from model import *
import os
from files import LoadFile

def main():
    '''Funcion principal del programa. Comienzo de la ejecucion'''
    fin = ''
    while(fin != '1'):
        flag = True
        print('INGRESE EL PATH DONDE DESEA REALIZAR LA BUSQUEDA')
        path = input()
        if os.path.exists(path):
            print('MODO DE CONSULTA. TECLEE 1 O 2:')
            print('1 - Casual')
            print('2 - Experto')
            queryMode = input()
            
            coincidence = '0'
            if(queryMode == '1'):
                print('TIPO DE COINCIDENCIA. TECLEE 1 O 2:')
                print('1 - TOTAL') #AND
                print('2 - PARCIAL') #OR
                coincidence = input() 
            print('INGRESE LA CONSULTA DESEADA')
            query = input()

            content = LoadFile(path)

            result = ExcecuteModel(content, query, queryMode, coincidence)

            print('\nRESULTADOS DE LA CONSULTA: \n')
            if(len(result) == 0):
                print('NO SE ENCONTRARON COINCIDENCIAS')
            for i, doc in enumerate(result):
                print(i, '-', doc)
            print('\n')
            flag = False
        
        if(flag):
            print('El path es invalido')
        print('TECLEE: ')
        print('1 - Salir')
        print('2 - Hacer otra consulta')
        fin = input()
    
if __name__ == '__main__':
    main()