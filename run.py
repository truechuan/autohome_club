import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from autohome_club.spiders.spider import AutohomeSpider

process = CrawlerProcess(get_project_settings())

process.crawl(AutohomeSpider)
process.start() # the script will block here until the crawling is finished