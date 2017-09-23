# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 22:05:24 2017
爬取6v电影网全部喜剧电影的第一层连接，并保存为txt格式的文档
其中的 CrawIP.bi 文件需要先运行IPpool进行爬去才能使用
@author: 陈仁祥
"""
#from bs4 import BeautifulSoup
from lxml import etree
import requests
import chardet
import random
#import re
import pickle
import time

#User_agent_list = []
#with open("./user_agent.txt","r") as fp_userAgent:
#    for line in fp_userAgent.readlines():
#        User_agent_list.append(line.split('\n')[0])
#with open('./user_agent.bi','wb') as fp_user:
#    pickle.dump(User_agent_list,fp_user)

#  预处理将ip序列化
#pattern = re.compile(r'\S*')
#with open("./crxIP.txt",'r') as fp_IP:
#    for each in fp_IP:
#        IPpool.append(pattern.search(each).group())
#with open("./IPpool.bat",'wb') as fp:
#    pickle.dump(IPpool,fp)  
def Crawhtml(IPpool,User_agent_list,url):
    proxy = random.choice(IPpool)
    proxies = {'http':'http://'+proxy,'https':'https://'+proxy}
    user_agent = random.choice(User_agent_list)
    headers = {'User-Agent':user_agent}
    try:   
        r = requests.get(url,headers=headers,proxies=proxies)
        r.encoding = chardet.detect(r.content)['encoding']
        return r.text
    except:
        return False
        

fp_IP = open("./CrawIP.bi","rb")
IPpool = pickle.load(fp_IP)
fp_IP.close()

fp_user = open('./user_agent.bi','rb')
User_agent_list = pickle.load(fp_user)
fp_user.close()


url_root = "http://www.6vhao.tv"
index = "dy1"

url_links =[]
for i in range(153): #153
    if bool(IPpool):
        i = i + 1
        print("正在爬取第%d个...."%(i))
        if i==1:
            url = url_root + r'/'+ index + r'/'
        else:
            url = url_root + r'/'+index + r'/' + 'index_' + str(i) + '.html'
            
        while bool(IPpool):
            user_agent = random.choice(User_agent_list)
            headers = {'User-Agent':user_agent}
            proxy = random.choice(IPpool)
            proxies = {'http':'http://'+proxy,'https':'https://'+proxy}
            try:
                r = requests.get(url,headers=headers,proxies=proxies,timeout=2)
                r.encoding = chardet.detect(r.content)['encoding']
                html = etree.HTML(r.text)
                link = html.xpath("//div[@class='listBox']/ul/li/div[@class='listimg']/a/@href")
                url_links.append(link)
                break
            except:
                IPpool.remove(proxy)
                print('Conection failed...')
        time.sleep(1)
    else:
        break
               
print("成功爬取%d条页面!"%i)
postfix = '.txt'
filename = './links_' + index + postfix
fp_link = open(filename,'w')
for each in url_links:
    for link in each:
        fp_link.write(link+'\n')
fp_link.close()

print("It's finished...")







