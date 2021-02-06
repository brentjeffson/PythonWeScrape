from wescrape.parsers.mparse import MangaParser
from wescrape.parsers.base import BaseParser
from wescrape.models.base import Selectors, Patterns, Source
import re

SOURCE_NAME = 'Fanfox'


class Fanfox(MangaParser):

    SOURCE = Source(
        root_url='http://fanfox.net/',
        image_base_url='',
        selectors=Selectors(
            title='div.detail-info p > span:nth-child(1)',
            thumbnail='div.detail-info > div.detail-info-cover > img',
            alt_titles='',
            authors='p.detail-info-right-say > a',
            genres='p.detail-info-right-tag-list > a',
            rating='div.detail-info p > span:nth-child(3) > span.item-score',
            description='p.detail-info-right-content',
            status='div.detail-info p > span:nth-child(2)',
            chapter='div#chapterlist li > a',
            upload_date='div#chapterlist li > a p:nth-child(2)',
            chapter_image='script;2'
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

        pattern = r'\'(\|.+)\'\.split'
        parts = re.findall(pattern, str(soup))[0].split('|')

        if len(parts) == 0:
            return image_urls

        root_url = '/'.join([
            f'{parts[8]}.{parts[7]}.{parts[12]}',
            parts[11],
            parts[10],
            parts[9],
            parts[6] + '.0',
            parts[3]
        ])
        for part in (parts):
            if re.match(r'\w\d+_\d+_\d+', part):
                image_urls.append('/'.join([root_url, part + f'.{parts[4]}']))

        return image_urls
