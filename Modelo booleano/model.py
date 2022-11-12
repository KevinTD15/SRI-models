import numpy as np
from tokenizer import *
from sympy import Symbol
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import to_dnf

reserved = ["|", "&", "~", "(", ")"]

def ToSymbol(normalizedQuery):
    result = []
    for i in normalizedQuery:
        if(i not in reserved):
            result.append(Symbol(f'{i}'))
            
def DocXTerm(normalizedContent):
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
    docs = []
    count = -1   
    for d in docXTerm[0]:
        count += 1
        for expr in exprList:
            flag = True
            for e in expr:
                ind = docXTerm[1].index(e.name)
                if(d[ind] != expr[e]):
                    flag = False  
                    break
            if(flag):
                docs.append(content[count])   
    return docs
        
def ExcecuteModel(content, query):
    normalizedContent = CleanAllTokens(content)
    normalizedQuery = NormalizeQuery(query)
    docXTerm = DocXTerm(normalizedContent)
    ToSymbol(normalizedQuery)
    queryFnd = to_dnf(normalizedQuery, True)
    exprList = CreateExpresionList(queryFnd)
    docs = SimFunc(docXTerm, exprList, content)
    return docs
    
    