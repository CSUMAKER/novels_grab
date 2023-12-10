"""
[使用模块]:  requests >>> pip install requests        <第三方模块>
            parsel >>> pip install parsel            <第三方模块>



"""

import os  # 内置模块 文件或文件夹
import time
import random
import requests  # 第三方的模块
import parsel  # 第三方的模块
from prettytable import PrettyTable# 第三方的模块
from selenium import webdriver# 第三方的模块
from selenium.webdriver.common.keys import Keys# 第三方的模块
from selenium.webdriver.common.by import By# 第三方的模块
from multiprocessing.dummy import Pool# 第三方的模块

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
    ]

def get_article(title,url):
    try:
        headers['user-agent'] = random.choice(user_agent_list)
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        # getall 返回的是一个列表 []
        book = selector.css('#chaptercontent::text').getall()
        book = '\n'.join(book)
        # 数据保存
        if os.path.exists(title + '.txt'):
            print('已下载章节:  ', title)
        else:
            with open(title + '.txt', mode='a', encoding='utf-8') as f:
                f.write(book)
                print('正在下载章节:  ', title)
    except Exception as e:
        print(e)


def get_toc(novel):
    link = novel[2]
    title_list = []
    url_list = []
    filename = '小说\\'+str(novel[1])+'\\'
    print("正在下载小说《"+str(novel[1])+"》")
    headers['user-agent'] = random.choice(user_agent_list)
    html_data = requests.get(url=link, headers=headers).text
    selector_2 = parsel.Selector(html_data)
    divs = selector_2.css('.listmain dd')
    if not os.path.exists(filename ):
        os.mkdir(filename)
    os.chdir(filename)
    for div in divs:
        
        title = div.css('a::text').get()
        href = div.css('a::attr(href)').get()
        url = 'https://www.bqg70.com' + href
        title_list.append(title)
        url_list.append(url)
    return title_list,url_list


def get_search_html():
    fiction = input("请输入要下载的小说：")
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_argument('headless')  # 设置option
    driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器
    driver.get('https://www.bqg70.com/')
    time.sleep(0.5)
    driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[1]/div[2]/form/input[1]').send_keys(fiction)
    driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[1]/div[2]/form/input[1]').send_keys(Keys.ENTER)
    original_window = driver.current_window_handle
    # 循环执行，直到找到一个新的窗口句柄
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    time.sleep(0.5)
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
    table = PrettyTable()
    table.title = 'novels'
    table.field_names = ["num","name","url"]
    table.add_rows(novels)
    print(table)
    return novels


def main():
    filename = '小说\\'
    if not os.path.exists(filename):
        os.mkdir(filename)
    html_data= get_search_html()
    while(True):
    # 解析html源码
        novels=get_novels(html_data)
        if  novels :
            break
    numbers_fiction = int(input("请输入要下载的小说编号（如果没有，输入0退出程序）："))
    if numbers_fiction == 0:
        return
    title_list,url_list=get_toc(novels[numbers_fiction-1])
    pool = Pool(100)  # 创建进程池
    for k in range(len(url_list)):
        pool.apply_async(get_article, (title_list[k],url_list[k]))
    pool.close()
    pool.join()
    return
    

if __name__ == "__main__":  # 当程序执行时
    main()
    
    
    
    
