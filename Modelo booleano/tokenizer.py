import nltk
from nltk.corpus import stopwords


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
        for word in stopwords.words('spanish'):
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
    for i in content:
        result.append(CleanToken(i[1]))
    return result