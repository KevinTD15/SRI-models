from unicodedata import numeric
import nltk
from nltk.corpus import stopwords
from tqdm import tqdm


def NormalizeDoc(s):
    replacements = (
        ("á","a"), ("é","e"), ("í","i"), ("ó","o"), ("ú","u"), ("-", " "), (".", " "), ("_", " ")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

def NormalizeQuery(s):
    replacements = (
        ("á","a"), ("é","e"), ("í","i"), ("ó","o"), (" o "," | "), (" y ", " & "), ("ú","u"), ("-", " "), (".", " "), 
        ("_", " "), (" no ", " ~ "), (" de ", " & ")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

def CleanToken(text, flag = False):
    if(flag):
        tokenize = nltk.word_tokenize(NormalizeQuery(text))
    else:
        tokenize = nltk.word_tokenize(NormalizeDoc(text))
    cleanToken = []
    save = True
    for i in tokenize:       #tqdm(tokenize):
        for word in stopwords.words('spanish'):
            #i = i.lower()
            if (word.lower() == i.lower()):
                #si existe no lo guarda
                save = False
        if (save):
            if (len(i) > 2):
                #guarda las palabras que no estan en stopwords y saca caracteres como: ".," etc
                cleanToken.append(i.lower())
        save = True
    return cleanToken
        
def CleanAllTokens(content):
    result = []
    for i in content:
        result.append(CleanToken(i))
    return result