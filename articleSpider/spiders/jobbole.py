# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
import time

from articleSpider.items import JobBoleArticleItem

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["web.jobbole.com"]
    start_urls = ("http://web.jobbole.com/all-posts/",)

    def parse(self, response):
        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        print("解析列表页中的所有文章url")
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            print("文章链接:",post_url)
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        # next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_url:
        #     print("下一页:",next_url)
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        #通过css选择器提取字段
        front_image_url = response.meta.get("front_image_url", "")  #文章封面图
        title = response.css(".entry-header h1::text").extract()[0]

        article_item['title'] = title
        article_item['front_image_url'] = [front_image_url]

        yield article_item
