from wescrape.parsers.mparse import MangaParser
from wescrape.parsers.base import BaseParser
from wescrape.models.base import Selectors, Patterns, Source
import json

SOURCE_NAME = 'Hentai2Read'


class Hentai2Read(MangaParser):

    SOURCE = Source(
        root_url='https://hentai2read.com/',
        image_base_url='https://static.hentaicdn.com/hentai/',
        selectors=Selectors(
            title='h3.block-title > a',
            thumbnail='div.img-container > a > img',
            authors='ul.list.list-simple-mini > li:nth-child(9)',
            genres='ul.list.list-simple-mini > li:nth-child(11)',
            description='p.detail-info-right-content',
            status='ul.list.list-simple-mini > li:nth-child(5)',
            chapter='ul.nav-chapters div.media > a',
            chapter_image='script::2'
        ),
        patterns=Patterns(
            index=r'[a-zA-Z.\s1-9]+[\s.]?[a-zA-Z]+[\s.]?([\d.]+)\s?\-?\s?[\w\d]+',
            upload_date=r'(\w{3})\s?(\d{2}),?\s?(\d{4})'
        )
    )

    def __init__(self, markup, parser='html.parser'):
        super().__init__(markup, self.SOURCE, parser)

    @classmethod
    def parse_chapter_images(cls, markup):
        soup = BaseParser(markup).soup
        image_urls = []
        selector = cls.SOURCE.selectors.chapter_image

        selector, idx = selector.split('::')
        tags = soup.find_all(selector)
        
        if len(tags) == 0:
            return image_urls

        try:
            json_obj = json.loads(
                ''.join(['{',
                    tags[int(idx)].string
                    .replace('var gData = {', '')
                    .replace('};', '')
                    .replace('\\', '')
                    .replace('\'', '"'),
                    '}'
            ]))
            image_urls = json_obj['images']
        except Exception as e:
            print(e)
            pass

        return image_urls
