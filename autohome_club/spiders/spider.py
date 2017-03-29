#!/usr/bin/env python
# encoding: utf-8
"""
@author: chenchuan@autohome.com.cn
@time: 2017/03/13
"""
# scrapy crawl XC60 --set LOG_FILE=log


from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import sys
from scrapy.http import Request
from autohome_club.items import AutohomeClubItem

default_encoding = 'utf-8'
domain = 'http://club.autohome.com.cn'

if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class AutohomeSpider(BaseSpider):
    name = "XC60"
    allowed_domains = ["autohome.com.cn"]

    start_urls = [
        "http://club.autohome.com.cn/bbs/forum-c-3411-1.html"
        #"http://club.autohome.com.cn/bbs/thread-c-3411-60039060-1.html"
    ]

    def completeUrl(self, _url):
        if not _url.startswith('http', 0, 4):
            _url = domain + _url
        return _url

    # 车系列表页
    def parse(self, response):
        hxs = Selector(response)
        urls = hxs.xpath('//div[@id="subcontent"]//a[@class="a_topic"]/@href')
        for url in urls:
            _url = self.completeUrl(url.extract())
            yield Request(_url, callback=self.parse_item)
        # 车系列表页分页
        page = hxs.xpath('//div[@class="pages"]//a[@class="afpage"]/@href')
        if page:
            next_page = self.completeUrl(page.extract()[0])
            yield Request(next_page, callback=self.parse)

    # 车系列表页 -> 论坛讨论页面
    def parse_item(self, response):
        items = []
        link = response.url

        hxs = Selector(response)
        title = hxs.xpath('//title/text()').extract()
        title = title[0].decode(default_encoding)

        contents = hxs.xpath('//div[contains(@class, "clearfix contstxt outer-section")]')
        f = open('log.txt', 'wb')

        for index, con in enumerate(contents):
            item = AutohomeClubItem()

            try:
                _text = self.getContext(con)

                _user_name = con.xpath('.//a[@xname="uname"]/text()').extract()[0]
                _user_name.decode(default_encoding)

                _date = con.xpath('.//span[@xname="date"]/text()').extract()[0]

                item['title'] = title
                item['link'] = link
                item['uname'] = _user_name
                item['content'] = _text
                item['date'] = _date
                items.append(item)
            except BaseException:
                print BaseException.message
                f.write(con.extract() + "\n")
            yield item

            # 论坛页分页
            page = hxs.xpath('//div[@class="pages"]//a[@class="afpage"]/@href')
            if page:
                next_page = self.completeUrl(page.extract()[0])
                yield Request(next_page, callback=self.parse_item)


    def getContext(self, con):
        if 0 != len(con.xpath('.//div[@class="w740"]//div[@class="yy_reply_cont"]').extract()):
            _text = con.xpath('.//div[@class="w740"]//div[@class="yy_reply_cont"]/text()').extract()[0]
        elif 0 == len(con.xpath('.//div[@class="w740"]/child::p').extract()):
            _text = con.xpath('.//div[@class="w740"]/text()').extract()[0]
        else:
            _text = con.xpath('.//div[@class="w740"]/child::p/text()').extract()[0]
        _text.decode(default_encoding)
        return _text
