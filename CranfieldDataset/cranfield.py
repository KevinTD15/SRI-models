import ir_datasets

dat = ir_datasets.load('cranfield')

def Qrels():
    qrels = []   
    for qr in dat.qrels_iter():
        qrels.append((int(qr.doc_id), int(qr.query_id)))
    return qrels

def Qtest():
    cranQuery = []   
    for q in dat.queries_iter():
        cranQuery.append(q.text)
    return cranQuery
        
def Dtest():
    content = []
    for doc in dat.docs_iter():
        content.append([doc.author + ' ' + doc.title, doc.author + ' ' + doc.title + ' ' + doc.text])
    return content