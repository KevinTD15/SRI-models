import numpy as np
from Utilities.tokenizer import *
from math import log10
from functools import lru_cache
from collections import Counter

def FreqTableQuery(normalizedQuery, terms):
    '''Tabla de frecuencia de los terminos de la query respecto a los del corpus'''
    cq = []#np.zeros(len(terms), int)
    flag = False
    mark = set()
    #term = list(terms)
    
    for i in normalizedQuery:
        flag = True
        if(i not in mark and i in terms):
            ind = terms.index(i)    
            cq.append([ind, normalizedQuery.count(i)])
            #cq[ind] = normalizedQuery.count(i)
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
    setList = []
    
    for i in normalizedContent:
        setList.append(set(i))
    
    for i in range(len(term)):
        for j in setList:
            if(term[i] in j):
                occurrence[i] += 1
                idf[i] = log10(len(normalizedContent)/occurrence[i])
                
    tfidfMod = [{} for x in range(len(normalizedContent))]
    for j in range(len(normalizedContent)):
        mark = set()
        if(len(normalizedContent[j]) > 0):
            maxV = Counter(normalizedContent[j]).most_common()[0][1]
            for k in normalizedContent[j]:
                if(k not in mark and k in terms):                   
                    ind = term.index(k)                    
                    tf[j][ind] = normalizedContent[j].count(k) / maxV
                    val = idf[ind] * tf[j][ind]
                    tfidfMod[j][ind] = val
                    mark.add(k)               
    return tfidfMod, term, idf

def NormalizeFTQuery(qft):
    '''Normaliza los terminos de la query'''
    maxV = max(qft, key=lambda item: item[1])
    for i in range(len(qft)):
        qft[i][1] = qft[i][1]/maxV[1]
    return qft

def TFxIDFQuery(qtf, idf):
    '''Se calcula la relevancia final'''
    result = []
    for i in range(len(qtf)):
        result.append([qtf[i][0], qtf[i][1] * idf[qtf[i][0]]])
    return result

   
def SimFunc(docs, query, content, index, umbral, normalizedCOntent, terms):
    '''Funcion de similitud donde se multiplica cada wij con los wiq'''
    result = []
    dq = []
    docAct = 0
    queryVec = [x[1] for x in query]
    for j in range(len(normalizedCOntent)):
        queryVecDot = []
        docVecDot = []
        for i in query:        
            if(terms[i[0]] in normalizedCOntent[j]):
                docVecDot.append(docs[j][i[0]])
                queryVecDot.append(i[1])
        dotProd = np.dot(queryVecDot, docVecDot)
        eucDistQ = np.linalg.norm(queryVec)
        eucDistD = np.linalg.norm(list(docs[j].values()))
        relevance = dotProd / (eucDistD * eucDistQ)
        if([content[docAct][0], relevance] not in result and relevance >= umbral):
            result.append([content[docAct][0], relevance])
            dq.append((docAct + 1, index + 1))
        docAct += 1
    result.sort(key=lambda x : x[1], reverse=True)
    return result, dq
                      
def ExcecuteModelV(content, query, umbral):
    '''inicio de la ejecucion del modelo'''  

    normalizedContent = CleanAllTokens(content)
    normalizedContent = tuple([tuple(x) for x in normalizedContent])
    wij, term, idf = FreqTable(normalizedContent)

    docsRes = []
    dqRes = []
    for q in range(len(query)):
        normalizeQuery = CleanToken(query[q], True)
        qft = FreqTableQuery(normalizeQuery, term)
        normalizedQft = NormalizeFTQuery(qft)
        wiq = TFxIDFQuery(normalizedQft, idf)        
        docs, dq = SimFunc(wij, wiq, content, q, umbral, normalizedContent, term)
        docsRes.append(docs)
        dqRes.append(dq)
    return docsRes, dqRes