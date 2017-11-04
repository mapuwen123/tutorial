# -*- coding: utf-8 -*-

import pymysql.cursors
from pymongo import MongoClient
from scrapy.exceptions import DropItem


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class TutorialPipeline(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.dbpool = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='py-spider',
            port=3306,
            charset='utf8'
        )

    def process_item(self, item, spider):
        db = self.client.runoob
        tieba_list = db.tieba_list
        message = tieba_list.find_one({'link': item['link']})
        if message:
            raise DropItem('与数据库重复')
        else:
            tieba_list_data = {
                'title': item['title'],
                'link': item['link']
            }
            result = tieba_list.insert_one(tieba_list_data)
            print('One post: {0}'.format(result.inserted_id))
        # return item
        cursor = self.dbpool.cursor()
        cursor.execute('select * from py_tieba_list where link=%s', item['link'])
        result = cursor.fetchall()
        if result:
            raise DropItem('与数据库重复')
        else:
            sql = 'insert into py_tieba_list(title,link) values (%s,%s)'
            cursor.execute(sql, (item['title'], item['link']))
            self.dbpool.commit()
        return item

    def close_spider(self, spider):
        self.client.close()
        self.dbpool.close()
