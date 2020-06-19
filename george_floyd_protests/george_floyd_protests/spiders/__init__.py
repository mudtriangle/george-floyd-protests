from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field
from bs4 import BeautifulSoup


class Song(Item):
    artist = Field()
    title = Field()
    lyrics = Field()


def parse_title(title_string):
    song = Song()

    title_list = title_string.split(' - ')
    title_list[1] = title_list[1].split(' (')
    title_list[1][0] = title_list[1][0].split(' [')

    song['artist'] = title_list[0].strip()
    song['title'] = title_list[1][0][0].strip()

    return song


class LyricsSpider(CrawlSpider):
    name = 'lyrics'
    allowed_domains = ['www.hhgroups.com']
    start_urls = ['http://www.hhgroups.com/letras/']

    rules = (Rule(LinkExtractor(allow=(), restrict_css=('.list_pag',)), callback='parse_page', follow=True),
             Rule(LinkExtractor(allow=(), restrict_css=('.tbl_oneline',)), callback='parse_song', follow=True),)

    @staticmethod
    def parse_page(response):
        pass

    @staticmethod
    def parse_song(response):
        soup = BeautifulSoup(response.body, features='lxml')

        for res in soup.find_all('p'):
            if '¿Tienes ya la letra para este tema? Ayúdanos y ¡' in res.get_text():
                print('Lyrics not found. Ignoring.')
                return

        web_title = soup.find('h1').get_text()
        song = parse_title(web_title)

        lyrics = soup.find('div', {'class': ['letra_body l17', 'letra_body l17 withEmbed']})\
            .find_all(text=True, recursive=False)

        if len(lyrics) == 0:
            paragraphs = soup.find('div', {'class': ['letra_body l17', 'letra_body l17 withEmbed']})\
                .find_all('p', recursive=False)

            lyrics = []
            for paragraph in paragraphs:
                lyrics += paragraph.find_all(text=True, recursive=False)

        song['lyrics'] = lyrics

        yield song