from tkinter import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import os
import re
import time
import random
import requests  # 第三方的模块
import parsel  # 第三方的模块
import _thread
from prettytable import PrettyTable# 第三方的模块
from selenium import webdriver# 第三方的模块
from selenium.webdriver.common.keys import Keys# 第三方的模块
from selenium.webdriver.common.by import By# 第三方的模块
from multiprocessing.dummy import Pool# 第三方的模块
root_path = os.path.dirname(__file__)
filedir =""
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0'
                      ' Safari/537.36',
    }
    # 随机UA
user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 "
        "Safari/537.36 Edg/100.0.1185.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 "
        "Safari/537.36 Edg/100.0.1185.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 "
        "Safari/537.36",
        'Mozilla/4.0(compatible; MSIE 6.0; Windows NT 5.1;SVl; QQDownload 732;.NET4.0C;.NET4.0E;LBBROWSER)',
        
        
    ]

def get_article(num,title,url):
    try:
        headers['user-agent'] = random.choice(user_agent_list)
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        # getall 返回的是一个列表 []
        book = selector.css('#chaptercontent::text').getall()
        book = '\n'.join(book)
        # 数据保存
        if os.path.exists(root_path+'\\'+num + '.txt'):
            print('已下载章节:  ', title)
        else:
            print('正在下载章节:  ', title)
            with open(num+ '.txt', mode='a', encoding='utf-8') as f:
                f.write(title+"\n"+book.replace("请收藏本站：https://www.qu70.cc。笔趣阁手机版：https://m.qu70.cc)",""))       
    except Exception as e:
        print(e)


def get_toc(novel):
    link = novel[2]
    title_list = []
    url_list = []
    filename = 'Download\\'+str(novel[1])+'\\'
    print("正在下载小说《"+str(novel[1])+"》")
    headers['user-agent'] = random.choice(user_agent_list)
    html_data = requests.get(url=link, headers=headers).text
    selector_2 = parsel.Selector(html_data)
    divs = selector_2.css('.listmain dd')
    if not os.path.exists(filename ):
        os.mkdir(filename)
    # os.chdir(filename)
    for div in divs:
        title = div.css('a::text').get()
        href = div.css('a::attr(href)').get()
        url = 'https://www.bqg70.com' + href
        title_list.append(title)
        url_list.append(url)
    return title_list,url_list


def get_search_html(fiction):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('headless')  # 设置option
    driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器
    # driver = webdriver.Chrome()  # 调用带参数的谷歌浏览器
    driver.get('https://www.bqg70.com/')
    time.sleep(1)
    driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[1]/div[2]/form/input[1]').send_keys(fiction)
    driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[1]/div[2]/form/input[1]').send_keys(Keys.ENTER)
    original_window = driver.current_window_handle
    # 循环执行，直到找到一个新的窗口句柄
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    time.sleep(1)
    # 获取当前窗口url
    current_url = driver.current_url
    # 获取当前窗口html源码
    html = driver.page_source
    driver.close()
    return html



def get_novels(html_data):
    selector_1 = parsel.Selector(html_data)
    novels=[]
    divs = selector_1.css('.bookinfo')
    for div in divs:
        novel=[]
        novel_name = div.css('a::text').get()
        href = div.css('a::attr(href)').get()
        novel_url = 'https://www.bqg70.com' + str(href)
        novel.append(divs.index(div)+1)
        novel.append(novel_name)
        novel.append(novel_url)
        novels.append(novel)
    # table = PrettyTable()
    # table.title = 'novels'
    # table.field_names = ["num","name","url"]
    # table.add_rows(novels)
    # print(table)
    return novels


# def 

 
def switch_window_load():
    def search():
        items = tr.get_children()
        for item in items:
            tr.delete(item)
        if  not str(text.get()) : 
            messagebox.showinfo("wanging","no")
        for i in range(10):
            html =get_search_html(str(text.get()))
        # 解析html源码
            novels=get_novels(html)
            if  novels :
                break
        if  not novels : 
            messagebox.showinfo("wanging","no")
        novels=get_novels(html)
        for novel in novels:
            print(novel[0],novel[1],novel[2])
            tr.insert("",index=END,text=novel[0],values=(novel[1],novel[2]))
            # time.sleep(0.05)
    # def load():
    #    tr.
    def load_novel(novel_index,novel_name,novel_url):
        filename = 'Download\\'+str(novel_name)+'\\'
        title_list,url_list=get_toc([novel_index,novel_name,novel_url])
        pool = Pool(10)  # 创建进程池
        for k in range(len(url_list)):
            # get_article(title_list[k],url_list[k])
            pool.apply_async(get_article, (filename+str(k).zfill(4),title_list[k],url_list[k]))
        pool.close()
        pool.join()
    
    def double_click(event):
        obj = event.widget
        iid = obj.identify("item",event.x,event.y)
        novel_index = obj.item(iid,"text")
        novel_name = obj.item(iid,"values")[0]
        novel_url = obj.item(iid,"values")[1]
        _thread.start_new_thread(load_novel,(novel_index,novel_name,novel_url,))
        return
    
    filename = 'Download\\'
    if not os.path.exists(filename):
        os.mkdir(filename)    
    top = Toplevel(root)
    top.title("小说下载器")
    top.geometry("1200x600+100+100") # 窗口大小
    top.maxsize(width=1200,height=800)#拖拽时最大窗口尺寸
    top.minsize(width=800,height=600)#拖拽时最小窗口尺寸
    
    toolbar = Frame(top,relief=RAISED,borderwidth=1)
    toolbar.pack(side=TOP,fill=X,pady=1)

    
    lb = Label(toolbar,text = "请输入要下载的小说：",anchor="center",font=("Helvetic" ,18 ,"bold"))
    lb.pack(side=LEFT)
    text = Entry(toolbar,width=60)
    text.pack(side=LEFT)
    
    Button(toolbar,text='搜索',command = lambda:_thread.start_new_thread(search,())).pack(side=LEFT,expand=True,fill=BOTH)
    
    
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=LEFT,fill=Y)

    tr = Treeview(top,columns=("novels","urls"),yscrollcommand=scrollbar.set)
    tr.heading("#0",text="Index")
    tr.heading("#1",text="novel")
    tr.heading("#2",text="url")
    tr.bind("<Double-1>",double_click)
    # lb.bind("<<ListboxSelect>>",item_select)
    tr.pack(side=LEFT,expand=True,fill=BOTH)
    scrollbar.config(command=tr.yview)
    # Button(toolbar,text='load').pack(side=LEFT,expand=True,fill=BOTH)
    # Button(toolbar,text='Save',command = save).pack(side=LEFT,expand=True,fill=BOTH)
    # 添加返回按钮
    btn_return = Button(toolbar, text='返回', command=lambda: top.destroy())
    btn_return.pack(side=LEFT,expand=True,fill=BOTH)
    
    
def switch_window_read():
    # # 销毁当前窗口
    # old_win.destroy()
    # 创建新的子窗口
    def load():
        global filedir
        # filename = filedialog.askopenfilename()
        filedir =filedialog.askdirectory()
        # os.chdir(filedir)
        filenames= os.listdir(filedir)
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
        
    top = Toplevel(root)
    top.title("简单文本阅读器")
    top.geometry("1200x600+100+100") # 窗口大小
    top.maxsize(width=1200,height=800)#拖拽时最大窗口尺寸
    top.minsize(width=800,height=600)#拖拽时最小窗口尺寸
    
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

    lb = Listbox(top,font=("Helvetic" ,10 ,"bold"),width=60,yscrollcommand=scrollbar.set)
    lb.bind("<<ListboxSelect>>",item_select)
    lb.pack(side=LEFT,expand=True,fill=BOTH)

    scrollbar.config(command=lb.yview)

    contents = ScrolledText(top,font=("Helvetic" ,20 ,"bold"))
    contents.pack(side = BOTTOM,expand=True,fill=BOTH)
    # filename = Entry()
    # filename.pack(side = LEFT,expand=True,fill=X)

    Button(toolbar,text='Open',command = load).pack(side=LEFT,expand=True,fill=BOTH)
    # Button(toolbar,text='Save',command = save).pack(side=LEFT,expand=True,fill=BOTH)
    # 添加返回按钮
    btn_return = Button(toolbar, text='返回', command=lambda: top.destroy())
    btn_return.pack(side=LEFT,expand=True,fill=BOTH)
    

root = Tk()
root.title("简单文本阅读器")
root.geometry("200x200+600+100") # 窗口大小
root.maxsize(width=1200,height=800)#拖拽时最大窗口尺寸
root.minsize(width=200,height=200)#拖拽时最小窗口尺寸
btn_load = Button(root, text='下载小说', command=lambda: switch_window_load())
btn_load.pack(pady=10)
btn_read = Button(root, text='阅读小说', command=lambda: switch_window_read())
btn_read.pack(pady=10)
mainloop()
