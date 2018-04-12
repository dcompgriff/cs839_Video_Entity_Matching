import numpy as np
import pandas as pd
import scrapy
from scrapy.shell import inspect_response
from string import ascii_uppercase


'''
Website: https://www.the-numbers.com/movies/letter/A
'''


class TheNumbersSpider(scrapy.Spider):
    name = "movies"
    start_urls=[]
    for c in ascii_uppercase:
        start_urls.append('https://www.the-numbers.com/movies/letter/'+c)
#    start_urls = ['https://www.the-numbers.com/movies/letter/A']
    headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, headers=self.headers)

    def moviepage_callback(self, response):
        rows=response.xpath('//div[@id="summary"]/table/tr')
        #the problem here is there is no fix format, need to do regex matching to find the mpaa rating etc
        rating_data=rows.xpath('.//td[contains(.,"MPAA")]/ancestor::tr')
        runningtime = rows.xpath('.//td[contains(.,"Running Time")]/parent::tr')
        #print("rating data is",rating_data.xpath('td[2]/a/text()').extract())
        #print("running time", runningtime.xpath('td[2]/text()').extract())
        cast_data = response.xpath('//div[@id="cast-and-crew"]//td[contains(.,"Director")]/parent::tr')
        actor_data = response.xpath('//div[@id="cast-and-crew"]//td[@itemprop="actor"]/parent::tr')
        #print("director ",cast_data.xpath('.//td[1]//span/text()').extract())
        finance_data = response.xpath('//table[@id="movie_finances"]//td[contains(.,"Worldwide")]/parent::tr')
        #print("finance data is", finance_data.xpath('.//td[2]/text()').extract())
        #try:
        #    yield {
        #            'mpaa': rating_data.xpath('td[2]/a/text()').extract()[0],
        #            'runtime': runningtime.xpath('td[2]/text()').extract()[0],
        #            'gross':finance_data.xpath('.//td[2]/text()').extract()[0],
        #            'director':cast_data.xpath('.//td[1]//span/text()').extract()[0]
        #            }
        #except:
        #    pass
        item = response.meta['item']
        rating = rating_data.xpath('td[2]/a/text()').extract()
        if len(rating)>0:
            item['mpaa'] = rating[0]
        else:
            item['mpaa']=""

        item['runtime']=""
        runtime=runningtime.xpath('td[2]/text()').extract()
        if len(runtime)>0:
            item['runtime'] = runtime[0]
        gross = finance_data.xpath('.//td[2]/text()').extract()
        item['gross']=""
        if len(gross)>0:
            item['gross']=gross[0]
        director=cast_data.xpath('.//td[1]//span/text()').extract()
        item['director']=""
        if len(director) >0:
            item['director'] = director[0]
        item['stars']=[]
        for actor in actor_data:
            try:
                item['stars'].append(actor.xpath('.//td[1]//span/text()').extract()[0])
            except:
                continue
        return item

    def parse(self, response):
        rows=response.xpath('//div[@id="wrap"]/div[@id="main"]/div[@id="page_filling_chart"]/center/table/tr')
        rows = rows[2:]
        for row in rows:
            try:
                item = {}
                item['title'] = row.xpath('td[2]/b/a/text()').extract()[0]
                item['release_date']=row.xpath('td[1]/text()').extract()[0]
                item['genres']=row.xpath('td[3]/a/text()').extract()
                item[ 'domestic gross'] = row.xpath('td[5]/text()').extract()[0]
                item['gross'] = row.xpath('td[5]/text()').extract()[0]
                item['director']=""
                item['stars']=""
                url=row.xpath('.//td[2]/b/a/@href').extract()
                if not url or len(url)<1:
                    yield item
                    continue
                url = 'https://www.the-numbers.com'+url[0]
                request=scrapy.Request(url, self.moviepage_callback, headers=self.headers)
                request.meta['item'] = item

                yield request
            except:
                continue
            #try:
            #    yield {
            #            'title': row.xpath('td[2]/b/a/text()').extract()[0],
            #            'release_date': row.xpath('td[1]/text()').extract()[0],
             #           'genres':row.xpath('td[3]/a/text()').extract(),
              #          'domestic gross': row.xpath('td[5]/text()').extract()[0],
               #         'gross': row.xpath('td[5]/text()').extract()[0],
                #        'director':"",
                 #       'stars':""
                  #      }
            #except:
            #    continue

        return

       # for url in response.xpath('//a/@href').extract():
       #                                        yield scrapy.Request(url, callback=self.parse)




















