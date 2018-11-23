import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import requests

class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Notices"
    
    def get_urls():
        year_urls = ['http://kenyalaw.org/kenya_gazette/gazette/year/'+str(year) for year in range(2005, 2019)]
        urls = []
        for url in year_urls:
            r = requests.get(url)
            bsObj = BeautifulSoup(r.text)
            urls.extend([link.get('href') for link in bsObj.find_all('a')])
        urls = list(set(urls))
        return [url for url in urls if 'http://kenyalaw.org/kenya_gazette/gazette/volume/' in url]
 
    def start_requests(self):
        for url in get_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # self.log(response.body)
        for div in response.xpath('//div[starts-with(@id,"GAZETTE NOTICE")]'):
            self.log('---START---\n')
            soup = BeautifulSoup(div.extract())
            self.log(soup.get_text().strip())
            self.log('---END--\n')
