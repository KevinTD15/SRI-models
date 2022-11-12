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
    for i in tokenize:
        for word in stopwords.words('spanish'):
            if (word.lower() == i.lower()):
                save = False
        if (save):
            if (len(i) > 2):
                cleanToken.append(i.lower())
        save = True
    return cleanToken
        
def CleanAllTokens(content):
    result = []
    for i in content:
        result.append(CleanToken(i))
    return result