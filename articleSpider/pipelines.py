# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs 
import json
import MySQLdb

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
# 图片下载的处理
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item

# 自定义json文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        print("item:",item)
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

#存储至数据库
class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('59.110.164.55','root','root','article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

        print("self.conn===========================================",self.conn)
    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, front_image_url)
            VALUES (%s, %s)
        """

        self.cursor.execute(insert_sql, (item["title"], item["front_image_url"]))
        self.conn.commit()
        


        