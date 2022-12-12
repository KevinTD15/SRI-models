from Utilities.tokenizer import *
from Models.vecModel import *
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

