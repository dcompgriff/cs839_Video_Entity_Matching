import numpy as np
import pandas as pd
import scrapy
from scrapy.shell import inspect_response



'''
Website: http://www.imdb.com/list/ls032600534/?sort=list_order,asc&st_dt=&mode=detail&page=1
'''


class IMDBSpider(scrapy.Spider):
    name = "movies"
    # Scrape Movies from page 1 through 43.
    start_urls = ['http://www.imdb.com/list/ls032600534/?st_dt=&mode=detail&sort=list_order,asc' + '&page=' +
                  str(i) for i in range(1, 44)]
    #start_urls = ['http://www.imdb.com/list/ls032600534/?st_dt=&mode=detail&sort=list_order,asc&page=1']
    #base_url = 'http://www.imdb.com'

    def parse(self, response):
        # Get the movie information from each movie item in the list.
        for movie in response.css('div.lister-item-content'):
            try:
                yield {
                    'title': movie.css('.lister-item-header').css('a::text').extract_first(),
                    'year': movie.css('.lister-item-header').css('span.lister-item-year::text').extract_first(),
                    'mpaa': movie.css('p.text-muted')[0].css('span.certificate::text').extract_first(),
                    'runtime': movie.css('p.text-muted')[0].css('span.runtime::text').extract_first(),
                    'genres': movie.css('p.text-muted')[0].css('span.genre::text').extract_first().strip().split(','),
                    'star_rating': movie.css('div.ratings-bar').css('div.ratings-imdb-rating::attr(data-value)').extract_first(),
                    'metascore_rating': movie.css('div.ratings-bar').css('div.ratings-metascore').css('span.metascore::text').extract_first(),
                    'description': movie.css('p')[1].css('p::text').extract_first(),
                    'director': movie.css('p.text-muted')[1].css('a')[0].css('a::text').extract_first(),
                    'stars': movie.css('p.text-muted')[1].css('a')[1:].css('a::text').extract(),
                    'gross': movie.css('p.text-muted')[2].css('span')[-1].css('span::text').extract_first(),
                }
            except:
                continue

        # Note, this serial method is slower than enumerating the set of start urls in a list.
        #inspect_response(response, self)
        # Traverse to next page if there is one.
        #next_page = response.css('a.lister-page-next').css('a::attr(href)').extract_first()
        #if next_page is not None:
        #    yield response.follow(self.base_url + next_page, self.parse)




















