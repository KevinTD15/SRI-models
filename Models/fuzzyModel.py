from Utilities.tokenizer import *
from Models.boolModel import *
from collections import Counter

def GetOcurrence(docXTerm, lenTerms):
    ocurrence = []
    for i in range(lenTerms):
        ocurr = Counter(docXTerm[:,i])
        ocurrence.append(ocurr[1])
    return ocurrence
    
def GetMultOcurrence(docXTerm, lenTerms):
    mulOcc = np.zeros((lenTerms, lenTerms), float)
    mark = np.zeros((lenTerms, lenTerms), bool)
    for i in range(lenTerms):
        for j in range(lenTerms):
            if(not mark[i][j]):
                count = 0
                a = docXTerm[:,i]
                b = docXTerm[:,j]
                for k in range(len(a)):
                    if(a[k] == 1 and b[k] == 1):
                        count +=1
                mulOcc[i][j] = count
                mulOcc[j][i] = count
                mark[i][j] = True
                mark[j][i] = True
    return mulOcc
       
def CreateCorrMatrix(docXTerm, terms):
    result = np.zeros((len(terms), len(terms)), float)    
    ocurrenceList = GetOcurrence(docXTerm, len(terms))
    multOcurrence = GetMultOcurrence(docXTerm, len(terms))
    
    for i in range(len(terms)):
        for j in range(len(terms)):
            result[i][j] = multOcurrence[i][j] / (ocurrenceList[i] + ocurrenceList[j] - multOcurrence[i][j])
    return result

def DegreeMembership(docXTerm, corrMatrix):
    result = np.zeros((len(docXTerm), len(corrMatrix)), float)

    for i in range(len(docXTerm)):
        for k in range(len(corrMatrix)):
            count = 1.0
            for h in range(len(corrMatrix[k])):
                if(count == 0):
                    break
                if(docXTerm[i][h] > 0):
                    count *= (1 - corrMatrix[k][h])
            result[i][k] = 1 - count
    return result

def ExcecuteModelF(content, query, queryMode, coincidence):
    normalizedContent = CleanAllTokens(content)
    if(queryMode == '2'):
        normalizedQuery = NormalizeQuery(query)
    elif(queryMode == '1'):
        cleanedQuery = CleanToken(query, True)
        normalizedQuery = ToAndForm(cleanedQuery)
    docXTerm, terms = DocXTerm(normalizedContent)
    corrMatrix = CreateCorrMatrix(docXTerm,terms)
    degMs = DegreeMembership(docXTerm, corrMatrix)
    ToSymbol(normalizedQuery)
    queryFnd = to_dnf(normalizedQuery)
    if((type(queryFnd) is And) and coincidence == '2'):
        exprList = CreateExpresionList(queryFnd)
    elif(type(queryFnd) is And) or (hasattr(queryFnd, 'name') and queryFnd.name != None):
        exprList = [satisfiable(queryFnd)]
    else:
        exprList = CreateExpresionList(queryFnd)
    a = 5