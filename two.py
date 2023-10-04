"""
[使用模块]: requests >>> pip install requests        <第三方模块>
           parsel >>> pip install parsel            <第三方模块>



"""

import os  # 内置模块 文件或文件夹
import time
import random

import requests  # 第三方的模块
import parsel  # 第三方的模块

filename = '小说\\'
if not os.path.exists(filename):
    os.mkdir(filename)

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
headers['user-agent'] = random.choice(user_agent_list)

rid = input('输入书名ID：')
link = f'https://www.bqg70.com/book/{rid}/'

html_data = requests.get(url=link, headers=headers).text
# print(html_data)
selector_2 = parsel.Selector(html_data)
divs = selector_2.css('.listmain dd')
novel_name = selector_2.css('.info h1').css('h1::text').get()
if not os.path.exists(filename + novel_name + '\\'):
    os.mkdir(filename + novel_name + '\\')
for div in divs:

    title = div.css('a::text').get()
    href = div.css('a::attr(href)').get()
    url = 'https://www.bqg70.com' + href
    try:
        headers['user-agent'] = random.choice(user_agent_list)
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        # getall 返回的是一个列表 []
        book = selector.css('#chaptercontent::text').getall()
        book = '\n'.join(book)
        # 数据保存
        if os.path.exists(filename + novel_name + '\\' + title + '.txt'):
            print('已下载章节:  ', title)
        else:
            with open(filename + novel_name + '\\' + title + '.txt', mode='a', encoding='utf-8') as f:
                # f.write(book)
                print('正在下载章节:  ', title)
    except Exception as e:
        print(e)
