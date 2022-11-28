from Models.vecModel import ExcecuteModelV
from Models.boolModel import ExcecuteModel
from Models.fuzzyModel import ExcecuteModelF
from Utilities.files import LoadFile 
import os
import ir_datasets

def main():
    '''Funcion principal del programa. Comienzo de la ejecucion'''
    fin = ''
    while(fin != '1'):
        flag = True
        cQuery = '2'
        
        print('Modelo')
        print('1 - BOOLEANO') #AND
        print('2 - VECTORIAL') 
        print('3 - FUZZY')
        mod = input()
        
        print('Desea usar la base de datos de CRANFIELD?')
        print('1 - Si')
        print('2 - No')
        cran = input()
        if(cran == '1'):
            print('TECLEE RANGO DE LOS DOCUMENTOS')
            low = int(input())
            up = int(input())
            content = []
            cranQuery = []
            dat = ir_datasets.load('cranfield')
            for doc in dat.docs_iter():
                content.append([doc.author + ' ' + doc.title, doc.author + ' ' + doc.title + ' ' + doc.text])
            for q in dat.queries_iter():
                cranQuery.append(q.text)
            
            content = content[low:up]
            
            print('DESEA USAR CONSULTAS DE CRANFIELD')
            print('1- Si')
            print('2- No')
            cQuery = input()
            
            if(cQuery == '1'):
                print('CUANTAS CONSULTAS REALIZAR. TECLEE UN RANGO DE NUMEROS')
                cantIni = input()
                cantEnd = input()
            
        else:
            print('INGRESE EL PATH DONDE DESEA REALIZAR LA BUSQUEDA')
            path = input()
            content = LoadFile(path)
            
        if cran == '1' or os.path.exists(path):
            
            if(mod == '1' or mod == '3'):
                multResults = []                    
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
                       
                if(cQuery == '2'):
                    print('INGRESE LA CONSULTA DESEADA')
                    query = input()
                    if(mod == '1'):
                        multResults.append(ExcecuteModel(content, query, queryMode, coincidence))
                    else:
                        multResults.append(ExcecuteModelF(content, query, queryMode, coincidence))
                else:
                    query = cranQuery[int(cantIni):int(cantEnd)]
                    for q in query:
                        if(mod == '1'):
                            multResults.append(ExcecuteModel(content, q, queryMode, coincidence))
                        else:
                            multResults.append(ExcecuteModelF(content, q, queryMode, coincidence))
                 
                for j in range(len(multResults)):
                    print(f'\nRESULTADOS DE LA CONSULTA: {query[j]}\n')
                    if(len(multResults[j]) == 0):
                        print('NO SE ENCONTRARON COINCIDENCIAS')
                    for i, doc in enumerate(multResults[j]):
                        if(doc[1] != 0):
                            print(i, '-', doc,  '\n') 
                
            elif(mod == '2'):
                multResults = []
                if(cQuery == '2'):
                    print('INGRESE LA CONSULTA DESEADA')
                    query = input()
                    multResults.append(ExcecuteModelV(content, query))
                else:                   
                    query = cranQuery[int(cantIni):int(cantEnd)]
                    for q in query:
                        multResults.append(ExcecuteModelV(content, q))                
                
                for j in range(len(multResults)):
                    print(f'\nRESULTADOS DE LA CONSULTA: {query[j]}\n')
                    if(len(multResults[j]) == 0):
                        print('NO SE ENCONTRARON COINCIDENCIAS')
                    for i in multResults[j]:
                        if(i[1] != 0):
                            print(f'Relevancia: {i[1]} --- Articulo: {i[0]}  \n')           
                
            flag = False
        
        if(flag):
            print('El path es invalido')
        print('TECLEE: ')
        print('1 - Salir')
        print('2 - Hacer otra consulta')
        fin = input()
    
if __name__ == '__main__':
    main()