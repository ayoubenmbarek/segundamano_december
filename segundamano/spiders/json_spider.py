import scrapy
import json
from ..items import SegundamanoItem 
from scrapy.spiders import CrawlSpider

def SegundamanoJsonSpider(CrawlSpider):
    name = "myspider"
    allowed_domains = ['webapi.segundamano.mx']
    handle_httpstatus_list = [301, 302, 502, 200]
    download_delay = 0
    download_timeout = 280
    start_urls = ['https://webapi.segundamano.mx/nga/api/v1/public/klfst?lang=es&category=1000&o=918713650,1515719403,8000&lim=5000']


    def parse(self, response):
        data = json.loads(response.body)
        cc = len(data.get('list_ads',[]))
        myItem = SegundamanoItem()
        myItem[ID_CLIENT] = cc
        yield myItem()
