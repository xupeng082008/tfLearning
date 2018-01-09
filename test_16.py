from bs4 import BeautifulSoup
import urllib.request
import time,re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import socket


socket.setdefaulttimeout(20) #对整个socket层设置超时时间。
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0')
    page = urllib.request.urlopen(req)  # 模仿浏览器登录
    txt = page.read().decode('utf-8')
    soup = BeautifulSoup(txt, 'lxml')
    return soup
#封装问题的链接
page_url =[]
for  num in range(1,45):
    url = 'https://www.zhihu.com/topic/20047590/questions?page={}'.format(num)
    soup = url_open(url)
    urllist = soup.find_all(attrs={'class': 'question-item-title'})
    time.sleep(10)
    for i in urllist:
        page =i.a['href']
        page_url.append('https://www.zhihu.com' + page)
def get_info(page_url):
    soup = url_open(page_url)
    titles= soup.find_all(attrs= {'class':'QuestionHeader-title'})[0].get_text()
    focus = soup.select('div.NumberBoard-value')[0].get_text()
    reviews = soup.select('div.NumberBoard-value')[1].get_text()
    frame = pd.DataFrame([titles, focus, reviews],
                         index=['titles', 'focus', 'reviews'])  # 转入数据列表
    frame = frame.T
    return frame

