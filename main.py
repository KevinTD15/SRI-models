from Models.vecModel import ExcecuteModelV
from Models.boolModel import ExcecuteModel
from Models.lsaModel import ExcecuteModelL
from Utilities.files import LoadFile 
from Crawler.exeCrawler import callCrawler
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
        print('3 - LSA')
        mod = input()
        
        print('Desea Crawlear')
        print('1 - Si')
        print('2 - No')
        crw = input()
        if(crw == '1'):
            print('Teclee tiempo limite (segundos) para el proceso')
            t = int(input())
            _, _ = callCrawler(t)
            direct = os.listdir('Crawler\cache')
            content = []
            for i in direct:
                a = open('Crawler/cache/'+i,encoding='utf8', errors='ignore')
                b = a.readlines()
                if(len(b) > 1):
                    content.append([b[0], b[1]])
            
        else:
        
            print('Desea usar la base de datos de CRANFIELD?')
            print('1 - Si')
            print('2 - No')
            cran = input()
            if(cran == '1'):
                content = []
                cranQuery = []
                dat = ir_datasets.load('cranfield')
                for doc in dat.docs_iter():
                    content.append([doc.author + ' ' + doc.title, doc.author + ' ' + doc.title + ' ' + doc.text])
                for q in dat.queries_iter():
                    cranQuery.append(q.text)

                print('DESEA USAR CONSULTAS DE CRANFIELD')
                print('1- Si')
                print('2- No')
                cQuery = input()
                
            else:
                print('INGRESE EL PATH DONDE DESEA REALIZAR LA BUSQUEDA')
                path = input()
                content = LoadFile(path)
            
        if crw == '1' or cran == '1' or os.path.exists(path):
            
            if(mod == '1'):
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
                    multResults = ExcecuteModel(content, query, queryMode, coincidence)
                    print(f'\nRESULTADOS DE LA CONSULTA: {query}\n')
                    for i in multResults:
                            if(i[1] != 0):
                                print(f'Articulo: {i}  \n')
                else:
                    query = cranQuery
                    for q in query:
                        multResults = ExcecuteModel(content, q, queryMode, coincidence)            
                        if(type(query) == list):
                            print(f'\nRESULTADOS DE LA CONSULTA: {q}\n')
                        else:
                            print(f'\nRESULTADOS DE LA CONSULTA: {q}\n')
                        if(len(multResults) == 0):
                            print('NO SE ENCONTRARON COINCIDENCIAS')
                        for i in multResults:
                            if(i[1] != 0):
                                print(f'Articulo: {i}  \n') 
                
            elif(mod == '2'):
                multResults = []
                if(cQuery == '2'):
                    print('INGRESE LA CONSULTA DESEADA')
                    query = input()
                    multResults = ExcecuteModelV(content, query)
                    print(f'\nRESULTADOS DE LA CONSULTA: {query}\n')
                    for i in multResults:
                            if(i[1] != 0):
                                print(f'Relevancia: {i[1]} --- Articulo: {i[0]}  \n')
                else:                   
                    query = cranQuery
                    for q in query:
                        multResults = ExcecuteModelV(content, q)            
                        if(type(query) == list):
                            print(f'\nRESULTADOS DE LA CONSULTA: {q}\n')
                        else:
                            print(f'\nRESULTADOS DE LA CONSULTA: {q}\n')
                        if(len(multResults) == 0):
                            print('NO SE ENCONTRARON COINCIDENCIAS')
                        for i in multResults:
                            if(i[1] != 0):
                                print(f'Relevancia: {i[1]} --- Articulo: {i[0]}  \n')   
            
            elif(mod == '3'):
                multResults = []
                print('TECLEE VALOR DE K')
                k = input()
                
                if(cQuery == '2'):
                    print('INGRESE LA CONSULTA DESEADA')
                    query = input()
                    multResults = ExcecuteModelL(content, [query], int(k))
                    print(f'\nRESULTADOS DE LA CONSULTA: {query}\n')
                    for i in multResults:
                        if(type(i) == list):
                            for j in i:
                                if(j[1] != 0):
                                    print(f'Relevancia: {j[1]} --- Articulo: {j[0]}  \n')
                        if(i[1] != 0):
                            print(f'Relevancia: {i[1]} --- Articulo: {i[0]}  \n')
                else:          
                    query = cranQuery         
                    multResults = ExcecuteModelL(content, query, int(k))              
                
                    for j in range(len(multResults)):
                        if(type(cranQuery) == list):
                            print(f'\nRESULTADOS DE LA CONSULTA: {query[j]}\n')
                        else:
                            print(f'\nRESULTADOS DE LA CONSULTA: {query}\n')
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