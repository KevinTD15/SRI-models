from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import filedialog
from Models.callModel import CallModel
from Utilities.files import ReadSimple
from Utilities.showDoc import Content

class View():
    def __init__(self):       
        #crear ventana principal
        self.root = Tk()
        self.root.title("Modelos de SRI")
        self.root.geometry("520x480"+"+"+str(10)+"+"+str(10)) 
        self.root.resizable(1,1)
        self.root.config(bg="lightblue",relief="sunken",bd=12) 
        self.menuBar = Menu(self.root)
        self.root.config(menu=self.menuBar)
        self.InitializeMenu()

        Label(text="Proyecto Final de SRI  2022\n\nIntegrante:\n Kevin Talavera Díaz C-311",bg="lightblue",fg="black",font=("arial",14),border=10,justify=CENTER).place(x=220,y=350)
        self.vr = None
        self.canvas = None
        self.mod = None
        self.path = StringVar()
        self.queryMode = StringVar(value='0') 
        self.crw = None
        self.time = None
        self.cran = None
        self.radio1 = None
        self.radio2 = None
        self.radio3 = None
        self.radio4 = None
        self.radio5 = None
        self.query = None
        self.k = IntVar(value=150)
        self.umbralS = DoubleVar(value=0.5)
        self.umbral = None
        self.cQuery = None
        self.cisi = None
        self.vaswani = None
        self.modelName = None
        self.coincidence = StringVar(value='0') 
        self.button = None 
        self.consult =None
        self.lcoincidence = None
        
        self.root.mainloop() 

    def InitializeMenu(self):        
        self.menuBar.add_cascade(label="Modelo Booleano", command=self.boolModel)
        self.menuBar.add_cascade(label="Modelo Vectorial", command=self.vecModel)
        self.menuBar.add_cascade(label="Modelo LSA", command=self.lsaModel)
        self.menuBar.add_cascade(label="Salir", command=self.root.quit)

    def CreateCanvas(self):
        self.canvas= Canvas(self.root,bd=0,bg="lightblue", relief="sunken",width=520,height=480)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        Label (text=self.modelName,bg="lightblue",fg="black",font=("arial",10)).place(x=150,y=20)

    def InputData(self):
        if self.canvas != None:
            self.canvas.destroy()
        self.CreateCanvas()  

        self.cQuery=StringVar(value="2")
        self.crw=StringVar()
        self.cran=StringVar()
        self.cisi=StringVar()
        self.consult=StringVar(value="0")

        self.radio1=Radiobutton(text="Crawling",bg="lightblue",fg="black",font=("arial",10), variable=self.consult, value='1',command=self.ReadCrawling)
        self.radio1.place(x=20,y=50)
        self.radio2=Radiobutton(text="Cranfield",bg="lightblue",fg="black",font=("arial",10), variable=self.consult, value='2',command=self.ReadDataset)
        self.radio2.place(x=120,y=50)
        self.radio3=Radiobutton(text="CISI",bg="lightblue",fg="black",font=("arial",10), variable=self.consult, value='3',command=self.ReadDataset)
        self.radio3.place(x=220,y=50)
        self.radio4=Radiobutton(text="Vaswani",bg="lightblue",fg="black",font=("arial",10), variable=self.consult, value='4',command=self.ReadDataset)
        self.radio4.place(x=300,y=50)
        self.radio5=Radiobutton(text="None",bg="lightblue",fg="black",font=("arial",10), variable=self.consult, value='5',command=self.SelectPath)
        self.radio5.place(x=380,y=50)

    def disableButton(self,radio345=False):
        self.radio1.configure(state="disable")
        self.radio2.configure(state="disable")
        if radio345:
            self.radio3.configure(state="disable")
            self.radio4.configure(state="disable")
            self.radio5.configure(state="disable")

    def ReadCrawling(self):
        self.disableButton(True)
        self.crw=StringVar(value='1')
        self.time=IntVar()
        Label(text="Teclee tiempo limite (segundos) para el proceso",bg="lightblue",fg="black",font=("arial",10)).place(x=20,y=100)
        Entry(width=3,textvariable=self.time).place(x=310,y=100)
        self.button = Button (text='ok',font=("arial",10),command=self.OtherInputData)
        self.button.place(x=350,y=60)
     

    def ReadDataset(self):
        self.disableButton(True)
        if(self.consult.get() == '4'):
            self.vaswani=StringVar(value='1')
        elif(self.consult.get() == '3'):
            self.cisi=StringVar(value='1')
        else:
            self.cran=StringVar(value='1')
        Label(text="Desea usar sus consultas ?:",bg="lightblue",fg="black",font=("arial",10)).place(x=20,y=100)
        self.radio1=Radiobutton(text="sí",bg="lightblue",fg="black",font=("arial",10), variable=self.cQuery, value='1', command=self.OtherInputData)
        self.radio1.place(x=300,y=100)
        self.radio2=Radiobutton(text="no",bg="lightblue",fg="black",font=("arial",10), variable=self.cQuery, value='2', command=self.OtherInputData)
        self.radio2.place(x=340,y=100)  

    def SelectPath(self):
            self.disableButton(True)  
            self.cQuery=StringVar(value='2')
            self.path.set("")
            Label (text="Seleccione path: ",font=("arial",10),bg="lightblue",fg="black").place(x=20,y=100)
            self.txtpath = Entry(textvariable=self.path,width=53)
            self.txtpath.place(x=125,y=100)
            Button (text='...',width=3,command=self.GetPath).place(x=448,y=95)
            self.OtherInputData()

    def GetPath(self):    
        self.path.set(filedialog.askdirectory(title='Escoja path', initialdir="C:"))
        #self.OtherInputData()

    def ReadCISI(self):
        self.disableButton(True)
        self.cisi=StringVar(value='1')
        pass

    def OtherInputData(self):
        self.disableButton()
        if self.cisi.get() == '1'  or self.crw.get() == '1' or self.cran.get() == '1' or self.path.get() is not None:
            if self.mod == '1':
                if self.cQuery.get() != '1': 
                    Label (self.canvas,text="Modo de consulta: ",bg="lightblue",fg="black",font=("arial",10)).place(x=20,y=140) 
                    self.radio1=Radiobutton(text="Casual",bg="lightblue",fg="black",font=("arial",10), variable=self.queryMode, value='1',command=self.QueryMode )
                    self.radio1.place(x=150,y=140)
                    self.radio2=Radiobutton(text="Experto",bg="lightblue",fg="black",font=("arial",10), variable=self.queryMode, value='2', command=self.QueryMode )
                    self.radio2.place(x=240,y=140)
                else:
                    self.QueryMode()
                self.TypeQuery()
            elif self.mod == '2':
                self.TypeQuery()
            elif self.mod == '3':
                Label(text="Teclee valor de K: ",bg="lightblue",fg="black",font=("arial",10)).place(x=20,y=140)
                Entry(textvariable=self.k,width=10).place(x=200,y=140)
                self.TypeQuery()    
                      
    def QueryMode(self):

        if self.queryMode.get() == '1' or self.cQuery.get() == '1' :
            self.lcoincidence= Label (text="Tipo de coincidencia: ",bg="lightblue",fg="black",font=("arial",10))
            self.lcoincidence.place(x=20,y=180)                
            self.radio1=Radiobutton(text="Total",bg="lightblue",fg="black",font=("arial",10), variable=self.coincidence, value='1',command=self.ExcecuteButton)
            self.radio1.place(x=150,y=180)
            self.radio2=Radiobutton(text="Parcial",bg="lightblue",fg="black",font=("arial",10), variable=self.coincidence, value='2',command=self.ExcecuteButton)
            self.radio2.place(x=240,y=180)
        elif self.lcoincidence is not None:    
            self.lcoincidence.destroy()
            self.radio1.destroy()
            self.radio2.destroy()

        self.ExcecuteButton()
    
    '''def Coincidence(self):
        self.radio1.configure(state="disable")
        self.radio2.configure(state="disable") 
        #self.TypeQuery()   ''' 
        
    def TypeQuery(self):
        if  self.cQuery.get() == '2':
            Label (text="Ingrese consulta deseada: ",font=("arial",10),bg="lightblue",fg="black").place(x=20,y=220)
            self.query = Text(width=58,height=3) 
            self.query.place(x=20,y=240)
        self.ExcecuteButton()   

    def boolModel(self):
        self.mod='1'
        self.modelName="MODELO BOOLEANO";
        self.InputData()

    def vecModel(self):
        self.mod='2' 
        self.modelName="MODELO VECTORIAL";
        self.InputData()

    def lsaModel(self):
        self.mod='3'
        self.modelName="MODELO SEMÁNTICA LATENTE";
        self.InputData()

    def ExcecuteButton(self):
        if self.mod!='1':
            Label(text="Teclee valor del umbral: ",bg="lightblue",fg="black",font=("arial",10)).place(x=20,y=180)
            Entry(textvariable=self.umbralS,width=10).place(x=200,y=180)  
        Button(text='Ejecutar',font=("arial",10),command=self.Excecute).place(x=200,y=320)
        
    def Excecute(self):
        Label(text="Espere ...",bg="lightblue",fg="black",font=("arial",10)).place(x=200,y=320)
        self.umbral=self.umbralS.get()
        
        result,p,r,f1value,cranQuery =CallModel(self)
        Label(self.root,text="BÚSQUEDA FINALIZADA",bg="lightblue",fg="black",font=("arial",12)).place(x=150,y=370)        
        Button(self.root,text='Reiniciar',font=("arial",10),command=self.InputData).place(x=200,y=420)
        if p!=None:
            l=Label(self.root,text=f'Precisión: {p}\nRecobrado: {r} \nF1: {f1value}',bg="lightblue",fg="black",font=("arial",10))
            l.place(x=140,y=320)
            self.ShowResult(result,cranQuery)
            
    def ShowResult(self,result,cranQuery):
        global crw
        global cran
        self.vr = Toplevel(self.root)
        self.vr.title("Resultado del " + self.modelName) 
        self.vr.geometry("610x500"+"+"+str(540)+"+"+str(10)) 
        self.vr.resizable(0,0)
        self.vr.config(bg="lightblue", bd=12, relief="sunken")
      
        hscrollbar = Scrollbar(self.vr, orient=HORIZONTAL)
        vscrollbar = Scrollbar(self.vr, orient=VERTICAL)

        resultList=  Listbox(self.vr, height=27, width=81, bg="black",fg="white",font=("arial",10),
                                 xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
        
        hscrollbar.config(command=resultList.xview)
        hscrollbar.pack(side=BOTTOM, fill=X)
        vscrollbar.config(command=resultList.yview)
        vscrollbar.pack(side=RIGHT, fill=Y)
              
        resultList.place(x=0,y=0)        
        resultList.config(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
              
        if self.mod=='1': #booleano
            if self.cQuery.get()=='2':
                resultList.insert(END ,'')
                resultList.insert(END ,f'CONSULTA: {self.query.get(1.0,"end-1c")}')
                for i in result:
                    for j in i:
                        if len(j)==0:
                            resultList.insert(END ,'NO SE ENCONTRARON COINCIDENCIAS')
                        else:
                            if j[1] != 0:
                                resultList.insert(END ,"Artículo: " + j)
            else:
                for j in range(len(result)):
                    resultList.insert(END ,'')
                    if(type(cranQuery) == list):
                        resultList.insert(END ,f'CONSULTA: {cranQuery[j]}')
                    else:
                        resultList.insert(END ,f'CONSULTA: {self.query.get(1.0,"end-1c")}')  
                    if  len(result[j])==0:
                        resultList.insert(END ,'NO SE ENCONTRARON COINCIDENCIAS')
                    else: #OJOOOO el ese lo puse yo preguntar
                        for i in result[j]:
                            if i[1] != 0:
                                resultList.insert(END ,"Artículo: " + i)
                        
        elif self.mod=='2':
            if self.cQuery.get()=='2':
                resultList.insert(END ,'')
                resultList.insert(END ,f'CONSULTA: {self.query.get(1.0,"end-1c")}')  
                for i in result:
                    for j in i:
                        if len(j)==0:
                            resultList.insert(END ,'NO SE ENCONTRARON COINCIDENCIAS')
                        else:  
                            if j[1] != 0:               
                                resultList.insert(END , f'Relevancia: {j[1]} --- Artículo: {j[0]}' )
            else:
                for j in range(len(result)):
                    resultList.insert(END ,'')
                    if(type(cranQuery) == list):
                        resultList.insert(END ,f'CONSULTA: {cranQuery[j]}')
                    else:
                        resultList.insert(END ,f'CONSULTA: {self.query.get(1.0,"end-1c")}')
                    if(len(result[j]) == 0):
                        resultList.insert(END ,'NO SE ENCONTRARON COINCIDENCIAS')
                    for i in result[j]:
                        if(i[1] != 0):
                            resultList.insert(END ,f'Relevancia: {i[1]} --- Artículo: {i[0]}') 
        elif self.mod=='3':
            if self.cQuery.get()=='2':
                resultList.insert(END ,'')
                resultList.insert(END ,f'CONSULTA: {self.query.get(1.0,"end-1c")}')  
                for i in result:
                    if type(i) == list:
                        for j in i:
                            if len(j)==0:
                                resultList.insert(END ,'NO SE ENCONTRARON COINCIDENCIAS')
                            else:
                                if j[1]!=0:
                                    resultList.insert(END ,f'Relevancia: {j[1]} --- Artículo: {j[0]}') 
            else:
                for j in range(len(result)):
                    resultList.insert(END ,'')
                    if type(cranQuery)==list:
                        resultList.insert(END ,f'CONSULTA: {cranQuery[j]}')  
                    else:
                        resultList.insert(END ,f'CONSULTA: {cranQuery}') 
                    if(len(result[j]) == 0):
                        resultList.insert(END ,'NO SE ENCONTRARON COINCIDENCIAS')
                    else:
                        for i in result[j]:
                            if(i[1] != 0):
                                resultList.insert(END ,f'Relevancia: {i[1]} --- Artículo: {i[0]}') 
        if self.cQuery.get()=='1':
            pass
        else:
            Label(text="                        ",bg="lightblue",height=5).place(x=200,y=320)                                
        Label(self.root,text="BÚSQUEDA FINALIZADA",bg="lightblue",fg="black",font=("arial",12)).place(x=150,y=370)        
        Button(self.root,text='Reiniciar',font=("arial",10),command=self.InputData).place(x=200,y=420)        

        crw = self.crw.get()
        cran = self.cran.get() if self.cran is not None else '0'
        
        selectedResult = 'Ningún elemento Seleccionado'
        resultList.bind('<<ListboxSelect>>', Select)
        self.vr.bind('<Return>', lambda ev:showinfo(title='text Seleccionado', message=selectedResult))

        self.vr.mainloop()

def Select(ev):
    global selectedResult
    global cran
    global crw
    selectedResult = ev.widget.get(ANCHOR)
    if(cran != '1'):
        if crw =='1':
            selectedResult = selectedResult[selectedResult.find('http'):len(selectedResult)]  
        else:
            selectedResult = selectedResult[selectedResult.find('Artículo: ')+10:len(selectedResult)]
    
        texto = ReadSimple(selectedResult)   
        if texto != None:
            Content(selectedResult,texto)
    

selectedResult = None    
crw = None
cran = None    

if __name__ == '__main__':
    app=View()