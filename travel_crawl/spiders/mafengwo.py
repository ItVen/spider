# -*- encoding:utf-8 -*-

import scrapy,requests,json,math,time,os,urllib,re
from bs4 import BeautifulSoup
from travel_crawl.items import TravelactivityItem
import socket  


class Data_Crawl(scrapy.Spider):

    def __init__(self):  
        self.headers = {  
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',  
            'Accept-Encoding':'gzip, deflate',  
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'  
        }  

    name = '8264'  #-爬虫名：一爬虫对应一名字
    allowed_domains = ["hd.8264.com"]  #不被过滤
    start_urls = ["xianlu-0-0-0-0-0-0-1-","xianlu-0-0-0-0-0-0-2-"]  #-开始爬取的url
    host = "http://hd.8264.com/"

    def start_requests(self):
        
        yield scrapy.Request(self.host + self.start_urls[0]+"1", meta={"type": 4}, callback=self.parse_pages)
        # yield scrapy.Request("http://hd.8264.com/xianlu-131168", meta={"type": 4}, callback=self.parse_info)

    def parse_pages(self, response):
        pages = response.xpath("//div[@class='dpfybox']/a/text()").extract()  
        total = re.findall(r'\d+', pages[9])
        t =int(total[0])+1
        for i in range(1,t):
            if i <= 10:
                print "%s%d------------------"%(self.start_urls[0],i)
                yield scrapy.Request(self.host + self.start_urls[0]+str(i), meta={"type": 4}, callback=self.parse_info)
            else:
                print "%s%d------------------"%(self.start_urls[1],i)
                yield scrapy.Request(self.host + self.start_urls[1]+str(i), meta={"type": 4}, callback=self.parse_info)

    def parse_info(self, response):
        infos = response.xpath("//div[@class='wonderful-list']/ul")
        type = response.meta["type"]
        if type == 4:
            for i in range(len(infos)):
               in_infos = infos[i].xpath(".//li").extract()
               for j in range(len(in_infos)):
                   soup = BeautifulSoup(in_infos[j], "html.parser")
                   item = TravelactivityItem()
                   item["price"] = soup.find(class_= "item-price").get_text()
                   item["info"] = soup.h3.get_text().replace("\n", "").replace(" ", "")
                   item["time"] = soup.find(class_= "item-time").get_text().split(" ")[0]
                   item["position"] = soup.find(class_= "item-time").get_text().split(" ")[1]
                   item['info_url'] = soup.a.get('href')  
                   item['info_img'] = soup.img.get("src").replace("!list2016325", "")
                   item['info_status'] = True 
                   # 详情页面抓取
                   yield scrapy.Request(url=soup.a.get('href'), meta={"type": type,"item": item}, callback=self.detail_view)

    def detail_view(self, response):
        #页面详情 获取更多图片文字数据以及发布机构信息
        data_item = response.meta["item"]
        type = response.meta["type"]
        if type == 4:
            print ("拉取详情页面---------------------%s")%response.url
            data = response.xpath("//div[@class='tm-ml-shim']").extract() #
            info_top = response.xpath("//ul[@class='crumbSlide-con']/li") #
            info_type = info_top[1].xpath(".//a/text()").extract()
            data_item['original_type'] = info_type[0]
            soup = BeautifulSoup('<html><head></head><body>' +data[0] + '</body></html>', 'lxml')
            provider = soup.find(class_ ="provider-name").get_text() #活动发起机构
            data_item['provider'] = provider
            time.sleep(5) #防止ip被封   
            yield data_item
   