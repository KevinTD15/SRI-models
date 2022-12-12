from CranfieldDataset.cranfield import Qrels, Dtest, Qtest
from CranfieldDataset.metrics import Evaluate, F1, F
from Models.vecModel import ExcecuteModelV
from Models.boolModel import ExcecuteModel
from Models.lsaModel import ExcecuteModelL
from Utilities.files import LoadFile 
from Crawler.exeCrawler import callCrawler
import os

def CallModel(app): #crw,time,cran,path,mod,cQuery,queryMode,coincidence,query,k

        if(app.crw.get() == '1'):
            _, _ = callCrawler(app.time.get())
            direct = os.listdir('Crawler\cache')
            content = []
            for i in direct:
                a = open('Crawler/cache/'+i,encoding='utf8', errors='ignore')
                b = a.readlines()
                if(len(b) > 1):
                    content.append([b[0], b[1]])           
        else:
            if(app.cran.get() == '1'):
                content = Dtest()
                cranQuery = Qtest()
                qrels = Qrels()  
                
            else:
                content = LoadFile(app.path.get())
            
        if app.crw.get() == '1' or app.cran.get() == '1' or os.path.exists(app.path.get()):
            
            if(app.mod == '1'):
                multResults = [] 
                       
                if(app.cQuery.get() == '2'): #ver si el query parametro es app. o no
                    multResults, _ = ExcecuteModel(content, [app.query.get(1.0,"end-1c")], app.queryMode.get(), app.coincidence.get())
                    return multResults,None,None,None,None

                else:
                    query = cranQuery
                    #for q in query:
                    multResults, dq = ExcecuteModel(content, query, app.queryMode.get(), app.coincidence.get())            
                    p, r = Evaluate(dq, qrels)
                    fValue = F(p, r)
                    f1Value = F1(p, r)
                    return multResults,p,r,f1Value,cranQuery
                
            elif(app.mod == '2'):
                multResults = []
                if(app.cQuery.get() == '2'):
                    multResults, _ = ExcecuteModelV(content, [app.query.get(1.0,"end-1c")],app.umbral)
                    return multResults,None,None,None,None
                else: 
                    multResults, dq = ExcecuteModelV(content,cranQuery,app.umbral)
                    p, r = Evaluate(dq, qrels)
                    fValue = F(p, r)
                    f1Value = F1(p, r)
                    return multResults,p,r,f1Value,cranQuery
            
            elif(app.mod == '3'):
                multResults = []

                if(app.cQuery.get() == '2'):
                    multResults, _ = ExcecuteModelL(content, [app.query.get(1.0,"end-1c")], app.k.get(),app.umbral)
                    return multResults,None,None,None,None

                else:          
                    query = cranQuery         
                    multResults, dq = ExcecuteModelL(content, query, app.k.get(),app.umbral) 
                    p, r = Evaluate(dq, qrels)
                    fValue = F(p, r)
                    f1Value = F1(p, r)
                    return multResults,p,r, f1Value, cranQuery
       
