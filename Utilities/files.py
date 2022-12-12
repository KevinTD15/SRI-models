from docx import Document
from PyPDF2 import PdfFileReader
import os, glob
import webbrowser

def readSimple(path):
    '''Funcion que recibe un path y devuelve solo su contenido (solo txt y doc(x))'''
    #if os.path.isfile(path):
    if path.endswith('.txt'):   return ReadTXT(path)
    elif path.endswith('.doc') or path.endswith('.docx'):   return ReadDOCX(path)
    else:
        webbrowser.open_new_tab(path)
    return None

def ReadTXT(path):
    '''Funcion que recibe un .txt y devuelve su contenido'''
    txt = open(path,'r')
    return txt.read()

def ReadDOCX(path):
    '''Funcion que recibe un .docx y devuelve su contenido'''
    doc = Document(path)
    texto = ''
    for lee in doc.paragraphs:
        texto += lee.text + "\n"
    return texto

def ReadPDF(path):
    '''Funcion que recibe un .pdf y devuelve su contenido'''
    pdf = PdfFileReader(path)
    texto = ''
    for lee in range(pdf.getNumPages()):
        texto += pdf.getPage(lee).extractText() + " "
    return texto
   
def Read(path):
    '''Funcion que recibe un path y devuelve ese path junto al contenido del documento(su nombre tambien se incluye)'''
    if os.path.isfile(path):
        index = path.rfind('\\')
        dotIndex = path.rfind('.')
        name = path[index + 1:dotIndex] + ' '
        if path.endswith('.txt'):
            return name+ ReadTXT(path)
        elif path.endswith('.doc') or path.endswith('.docx'):
            return name+ ReadDOCX(path)
        elif path.endswith('.pdf'):
            return name+ ReadPDF(path)
    return ""

def LoadFile(path):  
    '''Funcion que recibe el conjunto de path de los documentos y luego devuelve los documentos y su contenido asociado''' 
    ext = ['txt','docx','doc','pdf']
    docs = []
    for i in ext: 
        files = glob.glob(os.path.join(path, "*."+i), recursive=True)
        if len(files)>0:
            docs_text = [(doc_path , Read(doc_path),0) for doc_path in files]
            docs.extend(docs_text)           
    return docs