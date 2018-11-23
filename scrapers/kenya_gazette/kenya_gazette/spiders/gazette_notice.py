import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Notices"

    def url_generator(self,month,year):
        return 'http://kenyalaw.org/kenya_gazette/gazette/month/{}/{}'.format(month,year)
    def get_url_list(self,month_range=range(1,13),year_range=range(2006,2019)):
        url_list = []
        for m in month_range:
            for y in year_range:
                url_list.append(self.url_generator(m,y))
        return url_list
    def start_requests(self):
        urls = [
            'http://kenyalaw.org/kenya_gazette/gazette/volume/MTYzNA--/Vol.CXX-No.14',
            'http://kenyalaw.org/kenya_gazette/gazette/volume/OTIw/Vol.%20CXV%20-%20No.%2017',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # self.log(response.body)
        for div in response.xpath('//div[starts-with(@id,"GAZETTE NOTICE")]'):
            self.log('---START---\n')
            soup = BeautifulSoup(div.extract())
            self.log(soup.get_text().strip())
            self.log('---END--\n')
