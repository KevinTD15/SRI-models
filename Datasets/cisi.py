import os
import numpy as np
import pandas as pd

# for dirname, _, filenames in os.walk('D:\!!!UniVerSiDaD\IIIAno\SRI\Proyecto SRI\CranfieldDataset\CISI.ALL'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))
#        with open(os.path.join(dirname, filename)) as f:
#            line_count = 0
#            id_set = set()
#            for l in f.readlines():
#                line_count += 1
#                if filename == "CISI.REL":
#                    id_set.add(l.lstrip(" ").split(" ")[0])
#                elif l.startswith(".I "):
#                    id_set.add(l.split(" ")[1].strip())

def Dtest():        
    with open('D:\!!!UniVerSiDaD\IIIAno\SRI\Proyecto SRI\Datasets\CISI.ALL\CISI.ALL') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
        lines = lines.lstrip("\n").split("\n")

    doc_set = {}
    doc_id = ""
    doc_text = ""
    content = []
    for l in lines:
        if l.startswith(".I"):
            doc_id = l.split(" ")[1].strip()
        elif l.startswith(".T"):
            title = l[3:]
        elif l.startswith(".A"):
            autor = l[3:]
        elif l.startswith(".X"):
            doc_set[doc_id] = doc_text.lstrip(" ")
            content.append([autor + ' ' + title, autor +' '+ title + ' '+ doc_text.lstrip(" ")])
            doc_id = ""
            doc_text = ""
        else:
            doc_text += l.strip()[3:]
    return content
       
#print(f"Number of documents = {len(doc_set)}" + ".\n")
#print(doc_set["3"])

def Qtest(): 
    qry_set = {}
    qry_id = ""

    with open('D:\!!!UniVerSiDaD\IIIAno\SRI\Proyecto SRI\Datasets\CISI.ALL\CISI.QRY') as f:
        lines = ""
        for l in f.readlines():
            lines += "\n" + l.strip() if l.startswith(".") else " " + l.strip()
        lines = lines.lstrip("\n").split("\n")

    qry_set = {}
    qry_id = ""
    queries = []
    for l in lines:
        if l.startswith(".I"):
            qry_id = l.split(" ")[1].strip()
        elif l.startswith(".W"):
            qry_set[qry_id] = l.strip()[3:]
            queries.append(l.strip()[3:])
            qry_id = ""
    return queries
    
# Print something to see the dictionary structure, etc.
#print(f"Number of queries = {len(qry_set)}" + ".\n")
#print(qry_set["3"])

def Qrels():
    rel_set = {}
    qre = []
    with open('D:\!!!UniVerSiDaD\IIIAno\SRI\Proyecto SRI\Datasets\CISI.ALL\CISI.REL') as f:
        for l in f.readlines():
            qry_id = l.lstrip(" ").strip("\n").split("\t")[0].split(" ")[0]
            doc_id = l.lstrip(" ").strip("\n").split("\t")[0].split(" ")[-1]
            if qry_id in rel_set:
                rel_set[qry_id].append(doc_id)
            else:
                rel_set[qry_id] = []
                rel_set[qry_id].append(doc_id)
            qre.append((int(doc_id), int(qry_id)))
    return qre

#print(f"\nNumber of mappings = {len(rel_set)}" + ".\n")
#print(rel_set["7"])

a = 5