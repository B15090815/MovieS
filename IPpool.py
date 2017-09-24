# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 17:44:37 2017
爬取西刺国内普通代理的IP地址，并进行有效性测试
@author: 陈仁祥
"""

from lxml import etree
import requests
import random
import pickle
import time
def CrawIP():
    url = 'http://www.xicidaili.com/nt/'
    fp_user = open('./user_agent.bi','rb')
    User_agent_list = pickle.load(fp_user)
    fp_user.close()
    ips = []
    ports = []
    for j in range(2):
        print("正在获取%d页IP..."%(j+1))
        if j>0:
            url = url + str(j)
        headers = {'User-Agent':random.choice(User_agent_list)}
        r = requests.get(url,headers=headers)
        html = etree.HTML(r.text)
        ips.extend(html.xpath("//td[@class='country' and position()<2]/following-sibling::td[1]/text()"))
        ports.extend(html.xpath("//td[@class='country' and position()<2]/following-sibling::td[2]/text()"))
        time.sleep(5)
    #category = html.xpath("//td[@class='country' and position()<2]/following-sibling::td[5]/text()")
    for i in range(len(ips)):
        ips[i] = ips[i] + ':' + ports[i]
    
    useful = []
    test_url = 'https://www.baidu.com'
    k=1;
    for ip in ips:
        print('testing num %d....'%k,end='')
        k = k+1
        proxies = {'http':'http://'+ip,'https':'https://'+ip}
        headers = {'User-Agent':random.choice(User_agent_list)}
        try:
            r = requests.get(test_url,headers=headers,proxies=proxies,timeout=0.2)
            if r.status_code == 200:
                useful.append(ip)
                print('OK...')
        except:
            print('Failed...') 
    with open("./CrawIP.bi",'wb') as fp:
        pickle.dump(useful,fp)  
    print("It's finished...")
if __name__ == '__main__'  :
    CrawIP()
    
    