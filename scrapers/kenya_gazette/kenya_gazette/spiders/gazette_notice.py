import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import subprocess
import requests

class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Notices"

    def url_generator(self,month,year):
        return 'http://kenyalaw.org/kenya_gazette/gazette/month/{}/{}'.format(month,year)
    def generate_document_url(self,m,y):
        cur_url = self.url_generator(m, y)
        response = BeautifulSoup(requests.get(cur_url).text)
        response = response.find('div', attrs={'class': 'span9'})
        table = response.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            succeed = False
            for c, ele in enumerate(cols):
                if c == 1:

                    try:
                        href= ele.find_all('a', href=True)[0]['href']
                        succeed = True
                    except:
                        pass
                elif (c == 2) and succeed:
                    date=ele.text
        return href,date
    def get_url_list(self,month_range=range(1,13),year_range=range(2017,2019)):
        url_list = []
        date_list = []
        for m in month_range:
            for y in year_range:
                try:
                    cur_url,cur_date = self.generate_document_url(m,y)
                    url_list.append(cur_url)
                    date_list.append(cur_date)
                except:
                    pass
        return url_list,date_list
    def start_requests(self):
        #urls = [
        #    'http://kenyalaw.org/kenya_gazette/gazette/volume/MTYzNA--/Vol.CXX-No.14',
        #    'http://kenyalaw.org/kenya_gazette/gazette/volume/OTIw/Vol.%20CXV%20-%20No.%2017',
        #]

        urls,dates = self.get_url_list()
        #urls = ["http://kenyalaw.org/kenya_gazette/gazette/volume/MTc5NQ--/Vol.CVIII-No.57",]


        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # self.log(response.body)
        print(response.body)
        for div in response.xpath('//div[starts-with(@id,"GAZETTE NOTICE")]'):
            self.log('---START---\n')
            soup = BeautifulSoup(div.extract())
            self.log(soup.get_text().strip())
            self.log('---END--\n')
            print(soup)
if __name__ == '__main__':
    subprocess.call("scrapy crawl {}".format('"Gazette Notices"'))
    #g = GazetteNoticeSpider().get_url_list()