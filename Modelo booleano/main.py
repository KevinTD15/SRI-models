from os import listdir
from model import *

def main():
    fin = ''
    while(fin != '1'):
        print('INGRESE EL PATH DONDE DESEA REALIZAR LA BUSQUEDA')
        path = input()
        print('MODO DE CONSULTA. TECLEE 1 O 2:')
        print('1 - Casual')
        print('2 - Experto')
        queryMode = input()
        print('TIPO DE COINCIDENCIA. TECLEE 1 O 2:')
        print('1 - TOTAL') #AND
        print('2 - PARCIAL') #OR
        coincidence = input()
        print('INGRESE LA CONSULTA DESEADA')
        query = input()

        content = listdir(path)

        result = ExcecuteModel(content, query, queryMode, coincidence)

        print('\nRESULTADOS DE LA CONSULTA: \n')
        if(len(result) == 0):
            print('NO SE ENCONTRARON COINCIDENCIAS')
        for i, doc in enumerate(result):
            print(i, '-', doc)
        print('\n')
        
        print('TECLEE: ')
        print('1 - Salir')
        print('2 - Hacer otra consulta')
        fin = input()
    
if __name__ == '__main__':
    main()