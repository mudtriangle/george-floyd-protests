from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field
import scrapy
from bs4 import BeautifulSoup


WORDS_TO_IGNORE = ['Locations', 'See also', 'References', 'Further reading', 'External links']


class Song(Item):
    state = Field()
    loc = Field()
    description = Field()


class ProtestsSpider(CrawlSpider):
    name = 'protests'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_George_Floyd_protests_in_the_United_States']

    def parse(self, response):
        for href in response.css(".hatnote > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_descriptions)

    def parse_descriptions(self, response):
        soup = BeautifulSoup(response.body, features='lxml')
        state = soup.find('h1', {'class': 'firstHeading'}).get_text()

        locs = soup.find_all('span', {'class': 'mw-headline'})
        descs = soup.find_all('p')

        diff = 0
        last_i = 0
        protests = []
        for i in range(len(locs)):
            found = False
            for j in range(i, len(descs)):
                if locs[i].text.strip() in descs[j].text.strip():
                    diff = j - i
                    print(state[len('George Floyd protests in '):], diff)

                    for k in range(last_i, i + 1):
                        if locs[k].text not in WORDS_TO_IGNORE and len(locs[k].text) < 20:
                            try:
                                protests.append({'loc': locs[k].text.strip(),
                                                 'description': descs[k + diff].text.strip()})
                            except IndexError:
                                pass
                    
                    last_i = i + 1
            
            if found:
                break

        yield {state[len('George Floyd protests in '):]: protests}
