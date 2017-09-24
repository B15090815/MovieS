# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 10:37:20 2017

@author: 陈仁祥
"""
import pickle
import hashlib
import random
import chardet
import requests
import json
from lxml import etree

class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    def new_url_size(self):
        return len(self.new_urls)
    
    def old_url_size(self):
        return len(self.old_urls)
    
    def has_new_url(self):
        return self.new_url_size() !=0
    
    def get_new_url(self):
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        self.old_urls.add(url_md5)
        return new_url
    
    def add_new_url(self,url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)
            
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:           
            return
        for url in urls:
            self.add_new_url(url)
            
class Htmldownloader(object):
    def download(self,url):
        if url is None:
            return None
        fp_user = open('./user_agent.bi','rb')
        User_agent_list = pickle.load(fp_user)
        fp_user.close()
        
        fp_IP = open("./CrawIP.bi","rb")
        IPpool = pickle.load(fp_IP)
        fp_IP.close()
        
        while bool(IPpool):
            user_agent = random.choice(User_agent_list)
            headers = {'User-Agent':user_agent}
            proxy = random.choice(IPpool)
            proxies = {'http':'http://'+proxy,'https':'https://'+proxy}
            
            try:
                r = requests.get(url,headers=headers,proxies=proxies,timeout=2)
                if r.status_code == 200:
                    r.encoding = chardet.detect(r.content)['encoding']
                    return r.text
                else:
                    
                    return None
            except:
                print('connection failed...')
                IPpool.remove(proxy)
        return None


class DataOutput(object):
    def __init__(self):
        self.datas = []
    
    def data_input(self,data):
        if data is None:
            return
        self.datas.append(data)
    
    def data_save(self,filename):
        filename = filename + '.json'
        with open(filename,'w') as fp:
            json.dump(self.datas,fp=fp,ensure_ascii=False,indent=4)
            
 
class HtmlParser(object):
    def _get_new_urls(self,soup):
        new_urls = set()
        links = soup.xpath("//div[@class='listBox']/ul/li/div[@class='listimg']/a/@href")
        for link in links:
            new_urls.add(link)
        return new_urls
    
    def _get_new_data(self,soup):
        new_data = {}
        source = soup.xpath("//div[@id='text']")[0]
        img = source.xpath('./p[1]/img/@src')
        href = source.xpath('./table/tbody/tr/td/a/@href')
        title = soup.xpath('//div[@class="contentinfo"]/h1/a/text()')
        if title:
            title = title[0]
        else:
            title = 'NoBody'
        if img:
            new_data['image'] = img[0]
        else:
            new_data['image'] = 'Null'
        new_data['resource'] = href
        return {title:new_data}
    
    def parse(self,htmlContent,mode):
        soup = etree.HTML(htmlContent)
        if mode == 1:
            return self._get_new_urls(soup)
        elif mode == 2:
            return self._get_new_data(soup)
        else:
            return None
        
class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = Htmldownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
        
    def craw(self,root_url,mode,tp=1): 
        if mode==1:              
            self.manager.add_new_url(root_url)
        else:
            self.manager.add_new_urls(root_url)
#        while self.manager.has_new_url():
       
#        print(url)      
#        if bool(html):
        if tp==1:
            url = self.manager.get_new_url()
            html = self.downloader.download(url)
            if bool(html):
                links = self.parser.parse(html,tp)
                return links
            return None
        elif tp==2:
            k = 1;
            while self.manager.has_new_url():
                print("Woorking on num %d..."%k)
                k = k+1
                url = self.manager.get_new_url()
                html = self.downloader.download(url)
                if bool(html):
                    data = self.parser.parse(html,tp)
                    self.output.data_input(data)
            print("It's finished...")
            return


    def save_file(self,filename):
        self.output.data_save(filename)
            
if __name__ == '__main__':
    print('Start...')
    spider1 =  SpiderMan()
    spider2 =  SpiderMan()
    url_root = "http://www.6vhao.tv"  
    index = "dy1"
    all_link = set()
    for i in range(1): #153
        i = i + 1
        print("正在爬取第%d个...."%(i))
        if i==1:
            url = url_root + r'/'+ index + r'/'
        else:
            url = url_root + r'/'+index + r'/' + 'index_' + str(i) + '.html'
#        print(url)        
        links = spider1.craw(url,1)
        all_link = all_link | links
        
        
    print("第二层爬取开始...")   
    spider2.craw(all_link,2,2)
    spider2.save_file('dy1')
       
            
        
