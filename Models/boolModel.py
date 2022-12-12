import numpy as np
from Utilities.tokenizer import *
from sympy import And, Symbol
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import to_dnf
from functools import lru_cache
from typing import Dict as tDict, Any, Optional
import builtins
import types

reserved = ["|", "&", "~", "(", ")"]
DICT = tDict[str, Any]
keywordsSympy = {}

def loadKeywords(keywordsSympy: Optional[DICT] = None):
    exec('from sympy import *', keywordsSympy)
    builtins_dict = vars(builtins)
    for name, obj in builtins_dict.items():
        if isinstance(obj, types.BuiltinFunctionType):
            keywordsSympy[name] = obj

def eliminaKeywords(cadena, keywords):
    cadenaSinKeywords=""   
    band=False
    otrasKeys = ['else','round','input', 'Integer' ]
    
    if len(cadena)>0:
        for i in cadena.split(' '):
            if band: 
                band=False
                continue
            if  i in keywords or i in otrasKeys or (i[0]>='0' and i[0]<='9'):
                band=True
            else:
                if cadenaSinKeywords=="": 
                    cadenaSinKeywords=i
                else: 
                    cadenaSinKeywords=cadenaSinKeywords+' '+i
        if(band):
            cadenaSinKeywords = cadenaSinKeywords[0:len(cadenaSinKeywords) - 2]         
    return cadenaSinKeywords

def ToSymbol(normalizedQuery):
    '''Funcion donde cada palabra de la consulta e convierte en un simbolo'''
    result = []
    for i in normalizedQuery.split(' '):
        if(i not in reserved):
            result.append(Symbol(f'{i}'))
            
def ToAndForm(normalizedQuery):
    '''lleva una consulta en lenguaje natural a una consulta de solo AND entre sus terminos'''
    result = ''
    for i in normalizedQuery:
        if(i != normalizedQuery[len(normalizedQuery) - 1]):
            result += i + ' & '
        else:
            result += i
    return result

@lru_cache()      
def DocXTerm(normalizedContent):
    '''Se crea la matriz de documento contra ocurrencia o no de terminos'''
    terms = set()
    normalizedContent = list([list(x) for x in normalizedContent])
    
    for i in normalizedContent:
        terms.update(i)
    term = list(terms)
    
    cq = np.zeros((len(normalizedContent), len(term)), int)
    
    for i in range(len(normalizedContent)):
        mark = set()
        for j in normalizedContent[i]:
            if(j not in mark):
                ind = term.index(j)
                cq[i][ind] = 1
                mark.add(j)
      
    return cq, term

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

def SimFunc(docXTerm, exprList, content, q):
    '''Funcion de similitud del modelo booleano'''
    docs = []
    dq = []
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
                    dq.append((count + 1, q + 1))
    return docs, dq
        
def ExcecuteModel(content, query, queryMode, coincidence):
    '''Funcion principal de la ejecucion del modelo'''
    normalizedContent = CleanAllTokens(content)
    normalizedContent = tuple([tuple(x) for x in normalizedContent])
    docXTerm = DocXTerm(normalizedContent)
    loadKeywords(keywordsSympy)
    docs = []
    dq = []
    for q in range(len(query)):
        if(queryMode == '2'):
            normalizedQuery = NormalizeQuery(query[q])
        elif(queryMode == '1'):
            cleanedQuery = CleanToken(query[q], True)
            normalizedQuery = ToAndForm(cleanedQuery)
        normalizedQuery=eliminaKeywords(normalizedQuery,keywordsSympy)
        ToSymbol(normalizedQuery)
        queryFnd = to_dnf(normalizedQuery)
        if((type(queryFnd) is And) and coincidence == '2'):
            exprList = CreateExpresionList(queryFnd)
        elif(type(queryFnd) is And) or (hasattr(queryFnd, 'name') and queryFnd.name != None):
            exprList = [satisfiable(queryFnd)]
        else:
            exprList = CreateExpresionList(queryFnd)
        doc, dqpos = SimFunc(docXTerm, exprList, content, q)
        docs.append(doc)
        dq.append(dqpos)
    return docs, dq
    
    