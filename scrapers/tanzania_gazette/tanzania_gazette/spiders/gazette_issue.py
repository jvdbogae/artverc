import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from tanzania_gazette.items import TanzaniaGazetteItem

"Note that an html version of the gazette is not available for all listed years."
class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Issues"

    def create_urls(self):
        return ['http://www.utumishi.go.tz/utumishiweb/index.php?option=com_phocadownload&view=category&id=8:government-gazette&Itemid=179&lang=en']

    def start_requests(self):
        urls = self.create_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.collect_links)

    def collect_links(self, response):
        for a in response.xpath('//div[@class="pd-subcategory"]/a'):
            link = 'http://www.utumishi.go.tz' + a.xpath('@href').extract_first()
            name = a.xpath('text()').extract()
            request = scrapy.Request(url=link, callback=self.parse)
            request.meta['name'] = name
            yield request

    def parse(self, response):
        urls = []
        for url in response.xpath('//div[@class="pd-filename"]//a'):
            link = 'http://www.utumishi.go.tz' + url.xpath('@href').extract_first()
            urls.append(link)
            name = url.xpath('text()').extract()
            request = scrapy.Request(url=link, callback=self.download)
            request.meta['name'] = name
            yield request

    def download(self,response):
        return scrapy.FormRequest.from_response(
            response,
            callback=self.after_submit,
            meta={'name': response.meta['name']}
        )

    def after_submit(self, response):
        fileName = '/Users/Joachim/Downloads/' + response.meta['name'][0].replace(' ', '-').lower() + '.pdf'
        with open(fileName, 'wb') as f:
            f.write(response.body)


