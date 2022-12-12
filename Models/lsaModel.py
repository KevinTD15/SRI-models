from collections import Counter
from math import log10
from Utilities.tokenizer import *
import numpy as np

def GetVectors(S):
    result = []
    for i in range(len(S)):
        result.append([S[i], i])
    result.sort(key=lambda x : x[0])
    return result

def DeleteIndex(vecProps, value):
    result = []
    top = len(vecProps) - value
    for i in range(top):
        result.append(vecProps[i][1])
    return result

def ReduceS(S, indexToDelete):
    return np.delete(S, indexToDelete)
    
def ReduceVT(DT, indexToDelete):
    return np.delete(DT, indexToDelete, axis=0)

def ReduceU(T, indexToDelete):
    return np.delete(T, indexToDelete, axis=1)

def ReduceDim(U, S, VT, value):
    vecProps = GetVectors(S)
    indexToDelete = DeleteIndex(vecProps, value)
    Sr = ReduceS(S, indexToDelete)
    VTr = ReduceVT(VT, indexToDelete)
    Ur = ReduceU(U, indexToDelete)
    return Ur, Sr, VTr

def GetDocVector(DT):
    result = []
    for i in range(len(DT)):
        result.append([i, DT[i]])
    return result

def ToMatrix(Sr):
    result = np.zeros((len(Sr), len(Sr)), float)
    for i in range(len(Sr)):
        result[i][i] = Sr[i]
    return result

def Acomodar(VT, shape):
    return VT[0:shape[0], 0:shape[1]]

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

def SimFunc(docVec, queryVec, content, q, umbral):
    result = []
    countAct = 0
    dq = []
    for i in docVec:
        dotProd = np.dot(i[1], queryVec)
        eucDistQ = np.linalg.norm(queryVec)
        eucDistD = np.linalg.norm(i[1])
        relevance = dotProd / (eucDistQ * eucDistD)
        if([content[countAct][0]] not in result and relevance >= umbral):
            result.append([content[countAct][0], relevance])
            dq.append((countAct + 1, q + 1))
        countAct += 1
    result.sort(key=lambda x : x[1], reverse=True)
    return result, dq

def ExcecuteModelL(content, query, k, umbral):
    normalizedContent = CleanAllTokens(content)
    normalizedContent = tuple([tuple(x) for x in normalizedContent])
    wij, term, idf = FreqTable(normalizedContent)
    wijT = np.transpose(wij)
    wijT = np.nan_to_num(wijT)
    U, S, VT = np.linalg.svd(wijT)
    U = Acomodar(U, wijT.shape)
    if(k > len(S)):
        k = len(S) - 1
    Ur, Sr, VTr = ReduceDim(U, S, VT, k)
    Sr = ToMatrix(Sr)
    Vr = np.transpose(VTr)
    docVec = GetDocVector(Vr)
    Sinv = np.linalg.inv(Sr)
    UrT = np.transpose(Ur)
    aux = np.dot(Sinv, UrT)
    
    docs = []
    dq = []
    for q in range(len(query)):   
        normalizeQuery = CleanToken(query[q], True)
        qft = FreqTableQuery(normalizeQuery, term)
        normalizedQft = NormalizeFTQuery(qft)
        wiq = TFxIDFQuery(normalizedQft, idf) 

        queryVec = np.dot(aux, wiq)
        relevantDocs, dqpos = SimFunc(docVec, queryVec, content, q, umbral)
        docs.append(relevantDocs)
        dq.append(dqpos)
    return docs, dq

