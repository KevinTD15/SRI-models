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
    for i in indexToDelete:
        S = np.delete(S, i)
    return S
    
def ReduceVT(DT, indexToDelete):
    for i in indexToDelete:
        DT = np.delete(DT, i, axis=0)
        #DT = np.delete(DT, i, axis=1)
    return DT

def ReduceU(T, indexToDelete):
    for i in indexToDelete:
        T = np.delete(T, i, axis=1)
    return T

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

def SimFunc(docVec, queryVec, content):
    result = []
    countAct = 0
    for i in docVec:
        dotProd = np.dot(i[1], queryVec)
        eucDistQ = np.linalg.norm(queryVec)
        eucDistD = np.linalg.norm(i[1])
        relevance = dotProd / (eucDistQ * eucDistD)
        if([content[countAct][0]] not in result and relevance > 0):
            result.append([content[countAct][0], relevance])
        countAct += 1
    result.sort(key=lambda x : x[1], reverse=True)
    return result

def ExcecuteModelL(content, query, k):
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
        
        #ftT = np.transpose(ft)
        wijT = np.transpose(wij)
        wijT = np.nan_to_num(wijT)
        U, S, VT = np.linalg.svd(wijT)
        U = Acomodar(U, wijT.shape)
        Ur, Sr, VTr = ReduceDim(U, S, VT, k)
        Sr = ToMatrix(Sr)
        Vr = np.transpose(VTr)
        docVec = GetDocVector(Vr)
        Sinv = np.linalg.inv(Sr)
        UrT = np.transpose(Ur)
        #wiqT = np.transpose(wiq)
        aux = np.dot(Sinv, UrT)
        queryVec = np.dot(aux, wiq)
        docs = SimFunc(docVec, queryVec, content)
        return docs