#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import numpy as np
from scrapy.selector import Selector
from scrapy import signals
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import subprocess
import requests
import os
import re
import pandas as pd

class GazetteNoticeSpider(scrapy.Spider):
    name = "Gazette Notices"
    df = pd.DataFrame({'GAZETTE NOTICE': [], 'date': [], 'value': []})



    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        '''
        Add a callback when spider finish to save the database
        '''
        spider = super(GazetteNoticeSpider, self).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_closed)
        return spider
    def url_generator(self,month,year):
        '''
        Generate an url from month and year for kenya gazette url.
        '''
        return 'http://kenyalaw.org/kenya_gazette/gazette/month/{}/{}'.format(month,year)
    def parse_month_year_url(self,response):
        '''
        Process the url based on month and year and yield a scrapper request for href's in the table of the page.
        Keep the date in meta information (as dictionary).
        '''
        soup = BeautifulSoup(response.text)
        response = soup.find('div', attrs={'class': 'span9'})
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
            if succeed:
                yield scrapy.Request(url=href, callback=self.parse, meta={'date': date})
    # def generate_document_url(self,m,y):
    #     cur_url = self.url_generator(m, y)
    #     response = BeautifulSoup(requests.get(cur_url).text)
    #     response = response.find('div', attrs={'class': 'span9'})
    #     table = response.find('table')
    #     rows = table.find_all('tr')
    #     for row in rows:
    #         cols = row.find_all('td')
    #         succeed = False
    #         for c, ele in enumerate(cols):
    #             if c == 1:
    #
    #                 try:
    #                     href= ele.find_all('a', href=True)[0]['href']
    #                     succeed = True
    #                 except:
    #                     pass
    #             elif (c == 2) and succeed:
    #                 date=ele.text
    #     return href,date
    def start_requests(self,month_range=np.linspace(1,12,dtype=np.int8),year_range=np.linspace(2006,2018,dtype=np.int16)):
        '''
        Start the requests for the Kenya URL based on month. Give the range for analysis as input (month from 1 to 12 and year from 2006 and 2018.
        Be aware that if you use range method, it is an exclusive range. meaning that you need range(start,stop+1).
        '''

        for m in month_range:
            for y in year_range:
                try:
                    cur_url = self.url_generator(m,y)
                    yield scrapy.Request(url=cur_url, callback=self.parse_month_year_url)
                except:
                    pass

    # def start_requests(self):
    #     #urls = [
    #     #    'http://kenyalaw.org/kenya_gazette/gazette/volume/MTYzNA--/Vol.CXX-No.14',
    #     #    'http://kenyalaw.org/kenya_gazette/gazette/volume/OTIw/Vol.%20CXV%20-%20No.%2017',
    #     #]
    #
    #     urls,dates = self.get_url_list()
    #     #urls = ["http://kenyalaw.org/kenya_gazette/gazette/volume/MTc5NQ--/Vol.CVIII-No.57",]
    #
    #
    #     for url,date in zip(urls,dates):
    #         yield scrapy.Request(url=url, callback=self.parse, meta={'date': date})

    def parse(self, response):
        '''
        Parse the final url containing the gazette number and stock it inside a dataframe object (see pandas).
        '''
        for div in response.xpath('//div[starts-with(@id,"GAZETTE NOTICE")]'):
            self.log('---START---\n')
            soup = BeautifulSoup(div.extract())
            content = u'{}'.format(soup.get_text().replace('\n',' ').replace('\t',' ').replace('\r',' '))
            soup_id = soup.find('div').get('id')
            gazette_number = [int(s) for s in soup_id.split() if s.isdigit()][0]
            self.df = self.df.append({'GAZETTE NOTICE':gazette_number,'date':response.meta['date'].replace(" ",""),'value':content},ignore_index=True)
            self.log(soup.get_text().strip())
            self.log('---END--\n')
            yield {'GAZETTE NOTICE':gazette_number,'date':response.meta['date'].replace(" ",""),'value':content}

    def spider_idle(self, spider):
        '''
        Called when spider is finished. Save the dataframe into a csv file with line as gazette number. Columns are :
        gazette number, date and text. TODO Most probably, a cleaning of the text is needed.
        '''
        directory = os.getcwd() + '\\data\\'
        if not os.path.isdir(directory):
            os.makedirs(directory)
        self.df.to_csv(directory+'dataset.csv',sep=';')

if __name__ == '__main__':
    subprocess.call("scrapy crawl {}".format('"Gazette Notices"'))
    #g = GazetteNoticeSpider().get_url_list()