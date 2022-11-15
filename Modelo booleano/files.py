from docx import Document
from PyPDF2 import PdfFileReader
import os, glob

def ReadTXT(path):
    txt = open(path,'r')
    return txt.read()

def ReadDOCX(path):
    doc = Document(path)
    texto = ''
    for lee in doc.paragraphs:
        texto += lee.text + "\n"
    return texto

def ReadPDF(path):
    pdf = PdfFileReader(path)
    texto = ''
    for lee in range(pdf.getNumPages()):
        texto += pdf.getPage(lee).extractText() + " "
    return texto
   
def Read(path):
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
    txt_docs = glob.glob(os.path.join(path, "*.txt"), recursive=True)
    docs =  txt_docs
    docs_text = [(doc_path , Read(doc_path),0) for doc_path in docs]
    return docs_text