import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
<<<<<<< HEAD
from kenya_gazette.items import KenyaGazetteItem

"Note that an html version of the gazette is not available for all listed years."
class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Notices"

    def create_urls(self):
        urls = []
        for year in range(2018,2019):
        #for year in range(2018,2019):
            for month in range(1,13):
                url = 'http://kenyalaw.org/kenya_gazette/gazette/month/' + str(month) +'/' + str(year)
                urls.append(url)
        return urls

    def start_requests(self):
        url_year = 'http://kenyalaw.org/kenya_gazette/gazette/year/2018'
        url_month = 'http://kenyalaw.org/kenya_gazette/gazette/month/1/2018'

        urls = self.create_urls()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.collect_links)

    def collect_links(self, response):
        links = []
        for url in response.xpath('//div[contains(@class, "gazette-content")]//a/@href'):
            links.append(url.extract())
            yield scrapy.Request(url=url.extract(), callback=self.parse)


    def parse(self, response):
=======

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
>>>>>>> e4e7b24ae877b1dbb08f10449e6bc99eaeae507c
        for div in response.xpath('//div[starts-with(@id,"GAZETTE NOTICE")]'):
            self.log('---START---\n')
            soup = BeautifulSoup(div.extract())
            self.log(soup.get_text().strip())
<<<<<<< HEAD
            self.log('---END--\n')
            yield KenyaGazetteItem(text=soup.get_text().strip())

        for div in response.xpath('//div[re:test(@id, "\d{4}")]'):
            self.log('---START---\n')
            soup = BeautifulSoup(div.extract(), "lxml")
            self.log(soup.get_text().strip())
            self.log('---END--\n')
            yield KenyaGazetteItem(text=soup.get_text().strip())


=======
            self.log('---END--\n')
>>>>>>> e4e7b24ae877b1dbb08f10449e6bc99eaeae507c
