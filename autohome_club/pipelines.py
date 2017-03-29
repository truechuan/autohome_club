# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

rules_dice = "../rules.txt"


class AutohomeClubPipeline(object):
    def __init__(self):
        f = open(rules_dice)
        lines = f.readlines();
        rules = set()
        for line in lines:
            vals = line.split(",")
            for val in vals:
                rules.add(val)

        self.rules = rules
        self.used_file = codecs.open('XC60_used.json', 'wb', encoding='utf-8')
        self.unused_file = codecs.open('XC60_unused.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if item != {} and item['content'].strip() != "":
            unused_flag = True
            line = json.dumps(dict(item)) + '\n'
            for rule in self.rules:
                if rule in item['content'].strip():
                    self.used_file.write(line.decode("unicode_escape"))
                    unused_flag = False
                    break
            if unused_flag:
                self.unused_file.write(line.decode("unicode_escape"))
        return item
