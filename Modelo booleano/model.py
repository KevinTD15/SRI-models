import numpy as np
from tokenizer import *
from sympy import And, Symbol
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import to_dnf

reserved = ["|", "&", "~", "(", ")"]

def ToSymbol(normalizedQuery):
    '''Funcion donde cada palabra de la consulta e convierte en un simbolo'''
    result = []
    for i in normalizedQuery:
        if(i not in reserved):
            result.append(Symbol(f'{i}'))
            
def ToAndForm(normalizedQuery):
    result = ''
    for i in normalizedQuery:
        if(i != normalizedQuery[len(normalizedQuery) - 1]):
            result += i + ' & '
        else:
            result += i
    return result
            
def DocXTerm(normalizedContent):
    '''Se crea la matriz de documento contra ocurrencia o no de terminos'''
    terms = []
    for i in range(len(normalizedContent)):
        for j in normalizedContent[i]:
            if(j not in terms):
                terms.append(j)        
    
    cq = np.empty((len(normalizedContent), len(terms)), int)
    
    for i in range(len(terms)):
        for j in range(len(normalizedContent)):
            if(terms[i] in normalizedContent[j]):
                cq[j][i] = 1
            else:
                cq[j][i] = 0
    return cq, terms

def CreateExpresionList(queryFnd):
    '''Funcion que defuelve una lisa en la que en cada elemento hay una expresion de la FND'''
    exprList = []
    for i in queryFnd.args:
        expr = satisfiable(i)
        for e in expr:
            if(expr[e]):
                expr[e] = 1
            else:
                expr[e] = 0 
        exprList.append(expr)
    return exprList

def SimFunc(docXTerm, exprList, content):
    '''Funcion de similitud del modelo booleano'''
    docs = []
    count = -1   
    for d in docXTerm[0]:
        count += 1
        for expr in exprList:
            flag = True
            for e in expr:
                if(e.name in docXTerm[1]):
                    ind = docXTerm[1].index(e.name)
                    if(d[ind] != expr[e]):
                        flag = False  
                        break
                else:
                    flag = False
            if(flag):
                if(content[count][0] not in docs):
                    docs.append(content[count][0])   
    return docs
        
def ExcecuteModel(content, query, queryMode, coincidence):
    '''Funcion principal de la ejecucion del modelo'''
    normalizedContent = CleanAllTokens(content)
    if(queryMode == '2'):
        normalizedQuery = NormalizeQuery(query)
    elif(queryMode == '1'):
        cleanedQuery = CleanToken(query, True)
        normalizedQuery = ToAndForm(cleanedQuery)
    docXTerm = DocXTerm(normalizedContent)
    ToSymbol(normalizedQuery)
    queryFnd = to_dnf(normalizedQuery)
    if((type(queryFnd) is And) and coincidence == '2'):
        exprList = CreateExpresionList(queryFnd)
    elif(type(queryFnd) is And) or (hasattr(queryFnd, 'name') and queryFnd.name != None):
        exprList = [satisfiable(queryFnd)]
    else:
        exprList = CreateExpresionList(queryFnd)
    docs = SimFunc(docXTerm, exprList, content)
    return docs
    
    