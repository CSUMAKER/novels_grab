from tkinter import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter.ttk import *
import os
import re
filedir =""
  

# # 销毁当前窗口
# old_win.destroy()
# 创建新的子窗口
def load():
    global filedir
    # filename = filedialog.askopenfilename()
    filedir =filedialog.askdirectory()
    os.chdir(filedir)
    filenames= os.listdir(filedir)
    filenames.sort()
    for filename in filenames:
        lb.insert(END,filename)
        
    # contents.delete('1.0',END)
    # contents.insert(INSERT,file.read())
    

# def save():
#     with open (filename,'w',encoding='utf-8') as file:
#         file.write(contents.get('1.0',END))

def size_selected(event):
    f=Font(size=sizeVar.get())
    contents.configure(font=f)

def item_select(event):
    obj = event.widget
    index = obj.curselection()
    with open (obj.get(index),'r', encoding='utf-8',errors = 'ignore') as f:
        contents.delete('1.0',END)
        contents.insert(INSERT,f.read())
    
top = Tk()
top.title("简单文本阅读器")
top.geometry("600x600+600+100") # 窗口大小
top.maxsize(width=1200,height=800)#拖拽时最大窗口尺寸
top.minsize(width=200,height=200)#拖拽时最小窗口尺寸

toolbar = Frame(top,relief=RAISED,borderwidth=1)
toolbar.pack(side=TOP,fill=X,pady=1)

sizeVar=IntVar()
size = Combobox(toolbar,textvariable=sizeVar)
size_list = [x for x in range(8,30)]
size["value"]=size_list
size.current(20)
size.bind("<<ComboboxSelected>>",size_selected)
size.pack(side=LEFT)

scrollbar = Scrollbar(top)
scrollbar.pack(side=LEFT,expand=True,fill=Y)

lb = Listbox(top,font=("Helvetic" ,10 ,"bold"),yscrollcommand=scrollbar.set)
lb.bind("<<ListboxSelect>>",item_select)
lb.pack(side=LEFT,expand=True,fill=BOTH)

scrollbar.config(command=lb.yview)

contents = ScrolledText(font=("Helvetic" ,20 ,"bold"))
contents.pack(side = BOTTOM,expand=True,fill=BOTH)
# filename = Entry()
# filename.pack(side = LEFT,expand=True,fill=X)

Button(toolbar,text='Open',command = load).pack(side=LEFT,expand=True,fill=BOTH)
# Button(toolbar,text='Save',command = save).pack(side=LEFT,expand=True,fill=BOTH)
# 添加返回按钮

    
    
mainloop()

