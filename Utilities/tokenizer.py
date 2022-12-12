import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

def NormalizeDoc(s):
    '''Funcion que normaliza cada documento. Ej: si el doc tiene -á- sera sustituida por -a-'''
    replacements = (
        ("á","a"), ("é","e"), ("í","i"), ("ó","o"), ("ú","u"), ("-", " "), (".", " "), ("_", " "), ("/", " ")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

def NormalizeQuery(s):
    '''Funcion que normaliza la consulta y la lleva a una expresion booleana.'''
    replacements = (
        ("á","a"), ("é","e"), ("í","i"), ("ó","o"), (" o "," | "), (" y ", " & "), ("ú","u"), (".", " "), 
        ("_", " "), (" no ", " ~ "), (" de ", " & "), ("/", " "), ("-", " ")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

def CleanToken(text, flag = False):
    '''Funcion que elimina las palabras que -no aportan significado-, preposiciones, articulos, etc'''
    if(flag):
        #tokenize = (list(nltk.pos_tag(nltk.word_tokenize(NormalizeQuery(text)))))
        tokenize = nltk.word_tokenize(NormalizeQuery(text))
    else:
        #tokenize = (list(nltk.pos_tag(nltk.word_tokenize(NormalizeDoc(text)))))
        tokenize = nltk.word_tokenize(NormalizeDoc(text))
    cleanToken = []
    lemmatizer  = WordNetLemmatizer()
    stop = set(stopwords.words('english'))
    stop1 = set(stopwords.words('spanish'))
    stop = stop.union(stop1)
    for i in tokenize:
        i = lemmatizer.lemmatize(i)
        if not i.lower() in stop and "'" not in i:
            if (len(i) > 1):
                cleanToken.append(i.lower())
    return cleanToken
        
def CleanAllTokens(content):
    '''Funcion que itera por cada documento y llama a -CleanToken-'''
    result = []
    for i in content:
        result.append(CleanToken(i[1]))
    return result