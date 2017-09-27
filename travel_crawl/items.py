# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TravelactivityItem(scrapy.Item):
    position = scrapy.Field()  #活动位置
    time = scrapy.Field()      #活动出发时间
    info = scrapy.Field()      #活动 描述 图/文信息
    price = scrapy.Field()     #活动价格信息
    provider = scrapy.Field()   #活动发起机构
    info_url = scrapy.Field()   #活动详情页面
    info_img = scrapy.Field()   #活动展示图片
    info_status = scrapy.Field() #活动状态 开启/关闭
    original_type =  scrapy.Field() #活动类型
