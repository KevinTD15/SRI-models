import numpy as np
from Utilities.tokenizer import *
from math import log10
import time

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
    
def FreqTable(normalizedContent):
    '''Se crea la tabla de frecuencia'''
    terms = set()

    for i in normalizedContent:
        terms.update(i)
        
    term = list(terms)    

    cq = np.zeros((len(normalizedContent), len(terms)), int)

    for j in range(len(normalizedContent)):
        mark = set()
        for k in normalizedContent[j]:
            if(k not in mark):
                ind = term.index(k)
                cq[j][ind] = normalizedContent[j].count(k)
                mark.add(k)
    return cq, terms

def NormalizeFTQuery(qft):
    '''Normaliza los terminos de la query'''
    maxV = max(qft)
    return (list(map(lambda x: x / maxV, qft)))

def NormalizeFT(ft):
    '''se dividen las ocurrencias de cada termino de un documento entre la maxima ocurrencia'''
    maxV = []
    mappedFt = []
    for i in ft:
        maxV.append(max(i))
    
    for i in range(len(ft)):
        mappedFt.append(list(map(lambda x: x / maxV[i], ft[i])))
    
    return mappedFt

def TFxIDFQuery(qtf, idf):
    '''Se calcula la relevancia final'''
    result = []
    for i in range(len(qtf)):
        result.append(qtf[i] * idf[i])
    return result

def Idf(normalizedContent, term):
    '''se construye la tabla de idf'''
    docs = len(normalizedContent)
    result = np.zeros(len(term))
    for i in range(len(term)):
        nonZero = np.count_nonzero(normalizedContent[:,i])
        result[i] = log10(docs/ nonZero)
    return result

def TFxIDF(tf, idf):
    '''se calcula la importancia del termino i en el documento j para todo termino y documento'''
    cols = len(tf[0]) - 1
    tf = np.array(tf)
    for i in range(cols):
        tf[:, i] = list(map(lambda x: x * idf[i], tf[:,i]))
    return tf
   
def SimFunc(docs, query, content):
    '''Funcion de similitud donde se multiplica cada wij con los wiq'''
    result = []
    docAct = 0
    count = 0
    for i in docs:
        count += np.dot(i, query)
        # and count >= 0.1 poner esto en el if para sesgar las relevancias
        if([content[docAct][0], count] not in result and count >= 1):
            result.append([content[docAct][0], count])
        docAct += 1
        count = 0
    result.sort(key=lambda x : x[1], reverse=True)
    return result

def ExcecuteModelV(content, query):
    '''inicio de la ejecucion del modelo'''  
    start = time.time()
    normalizedContent = CleanAllTokens(content)
    normalizeQuery = CleanToken(query, True)
    
    ft, term = FreqTable(normalizedContent)
    qft = FreqTableQuery(normalizeQuery, term)
    
    if(type(qft) == int):
        return []
    else:   
        
        normalizedFt = NormalizeFT(ft)
        normalizedQft = NormalizeFTQuery(qft)

        idf = Idf(ft, term)

        wij = TFxIDF(normalizedFt, idf)
        wiq = TFxIDFQuery(normalizedQft, idf)
        
        docs = SimFunc(wij, wiq, content)
        return docs