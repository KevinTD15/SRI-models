import numpy as np
from Utilities.tokenizer import *
from math import log10

def FreqTableQuery(normalizedQuery, terms):
    '''Tabla de frecuencia de los terminos de la query respecto a los del corpus'''
    cq = np.zeros(len(terms), int)
    flag = False
    
    for i in range(len(terms)):
        if(normalizedQuery.count(terms[i]) > 0):
            flag = True
        cq[i] = normalizedQuery.count(terms[i])
    
    if(not flag):
        return 0
    return cq
    
def FreqTable(normalizedContent):
    '''Se crea la tabla de frecuencia'''
    terms = []
    for i in range(len(normalizedContent)):
        for j in normalizedContent[i]:
            if(j not in terms):
                terms.append(j) 
    cq = np.zeros((len(normalizedContent), len(terms)), int)
    
    for i in range(len(terms)):
        for j in range(len(normalizedContent)):
            cq[j][i] = normalizedContent[j].count(terms[i])
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
    docs = len(normalizedContent) - 1
    result = []
    for i in range(len(term)):
        count = 0
        for j in normalizedContent:
            if j[i] > 0:
                count += 1
        result.append(log10(docs/count))
    return result

def TFxIDF(tf, idf, term):
    '''se calcula la importancia del termino i en el documento j para todo termino y documento'''
    cols = len(tf[0]) - 1
    for i in range(cols):
        for j in range(len(tf)):
            tf[j][i] = tf[j][i] * idf[i]
    return tf
   
def SimFunc(docs, query, content):
    '''Funcion de similitud donde se multiplica cada wij con los wiq'''
    result = []
    docAct = 0
    for i in docs:
        count = 0
        for j in range(len(i)):
            count += query[j] * i[j]
        if([content[docAct][0], count] not in result and count >= 0.1):
            result.append([content[docAct][0], count])
        docAct += 1
    result.sort(key=lambda x : x[1], reverse=True)
    return result

def ExcecuteModelV(content, query):
    '''inicio de la ejecucion del modelo'''
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

        wij = TFxIDF(normalizedFt, idf, term)
        wiq = TFxIDFQuery(normalizedQft, idf)

        docs = SimFunc(wij, wiq, content)
        return docs