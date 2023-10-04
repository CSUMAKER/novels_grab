"""
[使用模块]: requests >>> pip install requests        <第三方模块>
           parsel >>> pip install parsel            <第三方模块>
           prettytable >>> pip install prettytable  <第三方模块>
[时间]:     2023/10/3
[编写]:     zxy

"""

import os  # 内置模块 文件或文件夹

import requests  # 第三方的模块
import parsel  # 第三方的模块


filename = '小说\\'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}


def get_toc(url):
    """
    获取每一章链接，储存到一个列表中并返回
    : url:小说目录页链接
    : return:每章链接
    """


def get_article(url):
    """
        获取每一章正文，并返回章节名和正文
        : url:小说章节链接
        : return:章节名，正文
        """


# 保存数据
def save_date(name, chapter, article, num):
    """
            保存数据
            :
            :
            """
    # 防止发生TXT文件写入错误
    file_path = name + '/' + str(num) + '.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(chapter + '\n')
        for s in article:
            f.write(s + '\n')


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    #    main()
    if not os.path.exists(filename):  # 创建“小说”文件夹
        os.mkdir(filename)
    rid = input('输入书名ID：')
    link = f'https://www.bqg70.com/book/{rid}/'

    html_data = requests.get(url=link, headers=headers).text
    # print(html_data)
    selector_2 = parsel.Selector(html_data)
    divs = selector_2.css('.listmain dd')
    for div in divs:
        title = div.css('a::text').get()
        href = div.css('a::attr(href)').get()
        url = 'https://www.bqg70.com' + href

        try:
            response = requests.get(url=url, headers=headers)
            selector = parsel.Selector(response.text)
            # getall 返回的是一个列表 []
            book = selector.css('#chaptercontent::text').getall()
            book = '\n'.join(book)
            # 数据保存
            with open(filename + title + '.txt', mode='a', encoding='utf-8') as f:
                f.write(book)
                print('正在下载章节:  ', title)
        except Exception as e:
            print(e)
