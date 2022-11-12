from os import listdir
from model import *

def main():
    print('INGRESE EL PATH DONDE DESEA REALIZAR LA BUSQUEDA')
    path = input()
    print('INGRESE LA CONSULTA DESEADA')
    query = input()
    
    content = listdir(path)
    
    result = ExcecuteModel(content, query)

    print(result)
    
if __name__ == '__main__':
    main()