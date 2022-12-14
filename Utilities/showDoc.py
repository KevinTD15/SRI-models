from tkinter import *

def Content(path, texto):
    
        vdoc = Tk()
        vdoc.title(path) 
        vdoc.geometry("610x500"+"+"+str(540)+"+"+str(10)) 
        vdoc.resizable(0,0)
        vdoc.config(bg="blue", bd=12, relief="sunken")
      
        '''hscrollbar = Scrollbar(vdoc, orient=HORIZONTAL)
        vscrollbar = Scrollbar(vdoc, orient=VERTICAL)

        resultList=  Listbox(vdoc, height=27, width=81, bg="black",fg="white",font=("arial",10),
                                 xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
        
        hscrollbar.config(command=resultList.xview)
        hscrollbar.pack(side=BOTTOM, fill=X)
        vscrollbar.config(command=resultList.yview)
        vscrollbar.pack(side=RIGHT, fill=Y)
              
        resultList.place(x=0,y=0)        
        resultList.config(xscrollcommand=hscrollbar.set, yscrollcommand=vscrollbar.set)
              
        resultList.insert(END ,texto)'''
        cuadroTexto = Text (vdoc)
        cuadroTexto.pack(fill="both",expand=1)
        cuadroTexto.config(bd=0,padx=0)
        cuadroTexto.delete(1.0,'end')
        cuadroTexto.insert('insert',texto)
        vdoc.mainloop()