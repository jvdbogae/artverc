import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup



import requests
year_urls = ['http://kenyalaw.org/kenya_gazette/gazette/year/'+str(year) for year in range(2005, 2019)]
urls = []
for url in year_urls:
    r = requests.get(url)
    bsObj = BeautifulSoup(r.text)
    urls.extend([link.get('href') for link in bsObj.find_all('a')])
urls = list(set(urls))
urls = [url for url in urls if 'http://kenyalaw.org/kenya_gazette/gazette/volume/' in url]



class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Notices"

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
