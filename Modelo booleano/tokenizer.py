import nltk
from nltk.corpus import stopwords
import time

def NormalizeDoc(s):
    '''Funcion que normaliza cada documento. Ej: si el doc tiene -á- sera sustituida por -a-'''
    replacements = (
        ("á","a"), ("é","e"), ("í","i"), ("ó","o"), ("ú","u"), ("-", " "), (".", " "), ("_", " ")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

def NormalizeQuery(s):
    '''Funcion que normaliza la consulta y la lleva a una expresion booleana.'''
    replacements = (
        ("á","a"), ("é","e"), ("í","i"), ("ó","o"), (" o "," | "), (" y ", " & "), ("ú","u"), ("-", " "), (".", " "), 
        ("_", " "), (" no ", " ~ "), (" de ", " & ")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

def CleanToken(text, flag = False):
    '''Funcion que elimina las palabras que -no aportan significado-, preposiciones, articulos, etc'''
    if(flag):
        tokenize = nltk.word_tokenize(NormalizeQuery(text))
    else:
        tokenize = nltk.word_tokenize(NormalizeDoc(text))
    cleanToken = []
    save = True
    for i in tokenize:
        for word in stopwords.words('english'):
            if (word.lower() == i.lower()):
                save = False
        if (save):
            if (len(i) > 1):
                cleanToken.append(i.lower())
        save = True
    return cleanToken
        
def CleanAllTokens(content):
    '''Funcion que itera por cada documento y llama a -CleanToken-'''
    result = []
    #if(len(content) > 0 and type(content[0]) == str):
    #    flag = True
    #else:
    #    flag = False
    start = time.time()
    end = 0
    for i in content:
        #if(not flag):
        #    result.append(CleanToken(i[1]))
        #else:
        if(end - start >= 99999999999):
            return result
        result.append(CleanToken(i[1]))
        end += time.time()
    return result