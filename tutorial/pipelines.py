# -*- coding: utf-8 -*-

import pymysql.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.dialects.mysql import pymysql


class TutorialPipeline(object):
    def __init__(self):
        self.dbpool = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='py-spider',
            port=3306,
            charset='utf8'
        )

    def process_item(self, item, spider):
        cursor = self.dbpool.cursor()
        sql = 'insert into py_tieba_list(title,link) values (%s,%s)'

        cursor.execute(sql, (item['title'], item['link']))
        self.dbpool.commit()
        return item
