from Datasets import cisi, cranfield, vaswani
from Datasets.metrics import Evaluate, F1
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
        elif(app.cisi.get() == '1'):
            content = cisi.Dtest()
            cranQuery = cisi.Qtest()
            qrels = cisi.Qrels() 
        elif(app.vaswani.get() == '1'):
            content = vaswani.Dtest()
            cranQuery = vaswani.Qtest()
            qrels = vaswani.Qrels() 
        else:
            if(app.cran.get() == '1'):
                content = cranfield.Dtest()
                cranQuery = cranfield.Qtest()
                qrels = cranfield.Qrels()  
                
            else:
                content = LoadFile(app.path.get())
            
        if app.vaswani.get() == '1' or app.cisi.get() == '1' or app.crw.get() == '1' or app.cran.get() == '1' or os.path.exists(app.path.get()):
            
            if(app.mod == '1'):
                multResults = [] 
                       
                if(app.cQuery.get() == '2'): 
                    multResults, _ = ExcecuteModel(content, [app.query.get(1.0,"end-1c")], app.queryMode.get(), app.coincidence.get())
                    return multResults,None,None,None,None

                else:
                    query = cranQuery
                    multResults, dq = ExcecuteModel(content, query, app.queryMode.get(), app.coincidence.get())            
                    p, r = Evaluate(dq, qrels)
                    f1Value = F1(p, r)
                    return multResults,p,r,f1Value,cranQuery
                
            elif(app.mod == '2'):
                multResults = []
                if(app.cQuery.get() == '2'):
                    multResults, _ = ExcecuteModelV(content, [app.query.get(1.0,"end-1c")],app.umbral.get())
                    return multResults,None,None,None,None
                else:
                    multResults, dq = ExcecuteModelV(content,cranQuery,app.umbral.get())
                    p, r = Evaluate(dq, qrels)
                    f1Value = F1(p, r)
                    return multResults,p,r,f1Value,cranQuery
            
            elif(app.mod == '3'):
                multResults = []

                if(app.cQuery.get() == '2'):
                    multResults, _ = ExcecuteModelL(content, [app.query.get(1.0,"end-1c")], app.k.get(),app.umbral.get())
                    return multResults,None,None,None,None

                else:          
                    query = cranQuery         
                    multResults, dq = ExcecuteModelL(content, query, app.k.get(),app.umbral.get()) 
                    p, r = Evaluate(dq, qrels)
                    f1Value = F1(p, r)
                    return multResults,p,r, f1Value, cranQuery
       
