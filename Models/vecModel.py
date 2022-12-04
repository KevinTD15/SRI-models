import numpy as np
from Utilities.tokenizer import *
from math import log10
from functools import lru_cache
from collections import Counter

def FreqTableQuery(normalizedQuery, terms):
    '''Tabla de frecuencia de los terminos de la query respecto a los del corpus'''
    cq = np.zeros(len(terms), int)
    flag = False
    mark = set()
    term = list(terms)
    
    for i in normalizedQuery:
        flag = True
        if(i not in mark and i in terms):
            ind = term.index(i)    
            cq[ind] = normalizedQuery.count(i)
            mark.add(i)
    
    if(not flag):
        return 0
    return cq

@lru_cache()
def FreqTable(normalizedContent):
    '''Se crea la tabla de frecuencia'''
    terms = set()

    normalizedContent = list([list(x) for x in normalizedContent])
    
    for i in normalizedContent:
        terms.update(i)
        
    term = list(terms)    

    idf = np.zeros(len(term), float)
    occurrence = np.zeros(len(term), int)
    tf = np.zeros((len(normalizedContent), len(term)), float)
    tfidf = np.zeros((len(normalizedContent), len(term)), float)
    setList = []
    
    for i in normalizedContent:
        setList.append(set(i))
    
    for i in range(len(term)):
        for j in setList:
            if(term[i] in j):
                occurrence[i] += 1
                idf[i] = log10(len(normalizedContent)/occurrence[i])
        
    for j in range(len(normalizedContent)):
        mark = set()
        if(len(normalizedContent[j]) > 0):
            maxV = Counter(normalizedContent[j]).most_common()[0][1]
            for k in normalizedContent[j]:
                if(k not in mark):
                    ind = term.index(k)                    
                    tf[j][ind] = normalizedContent[j].count(k) / maxV
                    tfidf[j][ind] = idf[ind] * tf[j][ind]
                    mark.add(k)               
    return tfidf, terms, idf

def NormalizeFTQuery(qft):
    '''Normaliza los terminos de la query'''
    maxV = max(qft)
    return (list(map(lambda x: x / maxV, qft)))

def TFxIDFQuery(qtf, idf):
    '''Se calcula la relevancia final'''
    result = []
    for i in range(len(qtf)):
        result.append(qtf[i] * idf[i])
    return result

   
def SimFunc(docs, query, content):
    '''Funcion de similitud donde se multiplica cada wij con los wiq'''
    result = []
    docAct = 0
    for i in docs:
        dotProd = np.dot(i, query)
        eucDistQ = np.linalg.norm(query)
        eucDistD = np.linalg.norm(i)
        relevance = dotProd / (eucDistQ * eucDistD)
        # and count >= 0.1 poner esto en el if para sesgar las relevancias
        if([content[docAct][0], relevance] not in result and relevance > 0):
            result.append([content[docAct][0], relevance])
        docAct += 1
    result.sort(key=lambda x : x[1], reverse=True)
    return result

def ExcecuteModelV(content, query):
    '''inicio de la ejecucion del modelo'''  

    normalizedContent = CleanAllTokens(content)
    normalizedContent = tuple([tuple(x) for x in normalizedContent])
    wij, term, idf = FreqTable(normalizedContent)

    normalizeQuery = CleanToken(query, True)
    qft = FreqTableQuery(normalizeQuery, term)
    normalizedQft = NormalizeFTQuery(qft)
    wiq = TFxIDFQuery(normalizedQft, idf)        
    docs = SimFunc(wij, wiq, content)
    
    return docs