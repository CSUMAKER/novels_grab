# -*- codeing = utf-8 -*-
#
"""
    2022/4/12
    编写：zxy
    """
import os
import re  # 正则表达式，进行文字匹配`
import requests
from lxml import etree
from multiprocessing.dummy import Pool


# def main():
# 获取网页

def get_toc(url):
    """
    获取每一章链接，储存到一个列表中并返回
    : url:小说目录页链接
    : return:每章链接
    """
    toc_html = requests.get(url, headers=headers)
    toc_url_list = []
    toc_url_block = re.findall('<dl(.*?)</dl>', toc_html.text, re.S)[0]
    selector = etree.HTML(toc_html.text)
    _name = selector.xpath('//*[@id="info"]/h1/text()')
    toc_url = re.findall('href="(.*?)"', toc_url_block, re.S)
    for n in toc_url:
        toc_url_list.append(url + n)
    return toc_url_list, _name[0]


def get_article(url):
    """
        获取每一章正文，并返回章节名和正文
        : url:小说章节链接,小说名，章节数
        : return:
        """
    chapter_html = requests.get(url[0], headers=headers)
    chapter_name = re.findall('<h1>(.*?)</h1>', chapter_html.text, re.S)
    print(chapter_name)
    selector = etree.HTML(chapter_html.text)
    info = selector.xpath('//*[@id="content"]/text()')
    saveData(url[1], chapter_name[0], info, url[2])


# 保存数据
def saveData(name, chapter, article, num):
    """
            保存数据
            :name, chapter, article, num：小说名，章节名，正文，章节数
            :return:
            """
    # 防止发生TXT文件写入错误
    file_path = '《' + name + '》' + '/' + str(num) + '.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(chapter + '\n')
        for s in article:
            f.write(s + '\n')
    f.close()


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    #    main()
    headers = {                             # 请求头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl'
                      'eWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
        'Host': 'www.bbiquge.net'
    }
    link = 'https://www.bbiquge.net/book_476/'  # 小说目录页链接
    r = requests.get(link, headers=headers, timeout=10)
    url_list, name_ = get_toc(link)             # 获取每一章链接和小说名
    os.makedirs('《' + name_ + '》', exist_ok=True)  # 创建文件夹
    pool = Pool(200)
    print('正在抓取' + '  ' + '《' + name_ + '》')
    article_list = [[x, x, x] for x in range(len(url_list))]
    for k in range(len(url_list)):
        article_list[k] = [url_list[k], name_, str(k)]
        # result = pool.map(get_article, article_list)
        # pool.close()
        pool.apply_async(get_article, (article_list[k],))
    pool.close()
    pool.join()
    print("爬取完毕！")
