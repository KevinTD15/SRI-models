import ir_datasets

dat = ir_datasets.load('vaswani')

def Qrels():
    qrels = []   
    for qr in dat.qrels_iter():
        if(int(qr.doc_id) <= 5500):
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
        content.append([doc.doc_id,doc.text])
    return content[0:5500]