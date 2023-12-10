from tkinter import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter.ttk import *
filename =""

def load():
    global filename 
    filename = filedialog.askopenfilename()
    with open (filename,'r', encoding='utf-8',errors = 'ignore') as file:
        contents.delete('1.0',END)
        contents.insert(INSERT,file.read())
     

def save():
    with open (filename,'w',encoding='utf-8') as file:
        file.write(contents.get('1.0',END))

def size_selected(event):
    f=Font(size=sizeVar.get())
    contents.configure(font=f)

top = Tk()
top.title("简单文本编辑器")

toolbar = Frame(top,relief=RAISED,borderwidth=1)
toolbar.pack(side=TOP,fill=X,pady=1)

sizeVar=IntVar()
size = Combobox(toolbar,textvariable=sizeVar)
size_list = [x for x in range(8,30)]
size["value"]=size_list
size.current(14)
size.bind("<<ComboboxSelected>>",size_selected)
size.pack(side=LEFT)

contents = ScrolledText()
contents.pack(side = BOTTOM,expand=True,fill=BOTH)
# filename = Entry()
# filename.pack(side = LEFT,expand=True,fill=X)

Button(text='Open',command = load).pack(side=LEFT)
Button(text='Save',command = save).pack(side=LEFT)


mainloop()
