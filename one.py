# -*- codeing = utf-8 -*-
#
"""
    2022/4/20
    编写：zxy
    """
import os
import re  # 正则表达式，进行文字匹配`
import time
import requests
from lxml import etree
from multiprocessing.dummy import Pool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    # 获取网页
    fiction = input("请输入要下载的小说：")
    link = get_url(fiction)  # 小说目录页链接
    # 返回小说目录页链接为空
    if not link:
        print("没有要搜索的小说！！！")
        return
    numbers_fiction = int(input("请输入要下载的小说编号（如果没有，输入0退出程序）："))
    if numbers_fiction == 0:
        return
    url_list, name_ = get_toc(link[numbers_fiction - 1])  # 获取每一章链接和小说名
    os.makedirs('《' + name_ + '》', exist_ok=True)  # 创建文件夹
    pool = Pool(200)  # 创建进程池
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
    return


def get_url(fiction):
    driver = webdriver.Chrome()
    driver.get('https://www.bbiquge.net/')
    time.sleep(2)
    driver.find_element('id', "bdcsMain").send_keys(fiction)
    driver.find_element('id', "bdcsMain").send_keys(Keys.ENTER)
    # Keys(driver).ADD("斗破苍穹")
    # ActionChains(driver).click(element).perform()
    original_window = driver.current_window_handle
    # 循环执行，直到找到一个新的窗口句柄
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    time.sleep(3)
    html = driver.page_source
    selector = etree.HTML(html)
    toc_block = re.findall('<tbody>(.*?)</tbody>', html, re.S)
    name_block = re.findall('<a(.*?)/a>', toc_block[0], re.S)
    url_list = re.findall('href="(.*?)">', toc_block[0], re.S)
    name_block[0] = '1'.join(name_block)
    name_list = re.findall('>(.*?)<', name_block[0], re.S)
    print("%-10s\t\t%-20s\t\t%-25s\t\t%-20s\t\t%-20s\t\t%-20s\t\t" % ('编号', '文章名称', '最新章节',
                                                                      '作者', '更新', '状态'))
    for i in range(int(len(name_list)) // 2):
        _list = selector.xpath('//*[@id="main"]/table/tbody/tr[' + str(i + 2) + ']/td/text()')
        print("%-10s\t\t%-20s\t\t%-25s\t\t%-20s\t\t%-20s\t\t%-20s\t\t" % (
            str(i + 1), name_list[2 * i], name_list[2 * i + 1],
            _list[0], _list[2], _list[3]))
    # 关闭标签页或窗口
    driver.close()
    # 切回到之前的标签页或窗口
    driver.switch_to.window(original_window)
    driver.close()
    return url_list[0:len(url_list):2]


def get_toc(url):
    """
    获取每一章链接，储存到一个列表中并返回
    : url:小说目录页链接
    : return:每章链接
    """
    toc_html = requests.get(url, headers=headers, timeout=10)
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
    return


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
    return


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    headers = {  # 请求头
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl'
                      'eWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
        'Host': 'www.bbiquge.net'
    }
    main()
