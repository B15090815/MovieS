# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 22:05:24 2017

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
        

#fp_IP = open("./IPpool.txt","rb")
#IPpool = pickle.load(fp_IP)
#fp_IP.close()

fp_user = open('./user_agent.bi','rb')
User_agent_list = pickle.load(fp_user)
fp_user.close()

proxy = '183.157.181.186:80'
proxies = {'http':'http://'+proxy,'https':'https://'+proxy}

url_root = "http://www.6vhao.tv"
index = "/dy1/"
#print(url_root+index)
#url_links = []
fp_links = open("./url_links.txt","w")
for i in range(10):
    i = i + 1
    print("正在爬去第%d个...."%(i))
    if i==1:
        url = url_root + index
    else:
        url = url_root + index + 'index_' + str(i) + '.html'
        
#    content = Crawhtml(IPpool,User_agent_list,url)
#    while not content:
#        content = Crawhtml(IPpool,User_agent_list,url)
#    html = etree.HTML(content)
    user_agent = random.choice(User_agent_list)
    headers = {'User-Agent':user_agent}  
    r = requests.get(url,headers=headers,proxies=proxies)
    r.encoding = chardet.detect(r.content)['encoding']
    html = etree.HTML(r.text)
    for item in html.xpath("//div[@class='listBox']/ul/li/div[@class='listimg']/a/@href"):
        item = item + '\n'
        fp_links.write(item)
#        url_links.append(item)
    time.sleep(5)
fp_links.close()
print("It'ok!")







