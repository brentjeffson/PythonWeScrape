from wescrape.parsers.mparse import MangaParser
from wescrape.models.base import Selectors, Patterns, Source
import re

SOURCE_NAME = 'Mangakatana'


class Mangakatana(MangaParser):

    SOURCE = Source(
        root_url='http://mangakatana.com/',
        image_base_url='',
        selectors=Selectors(
            title='div.info > h1.heading',
            thumbnail='div.cover > img',
            alt_titles='ul.meta > li:nth-child(1) > div:nth-child(2) > div.alt_name',
            authors='ul.meta > li:nth-child(2) > div:nth-child(2) > a',
            genres='ul.meta > li:nth-child(3) > div:nth-child(2) > div.genres > a',
            description='div.summary > p',
            status='ul.meta > li:nth-child(4) > div:nth-child(2)',
            chapter='div.chapters div.chapter > a',
            upload_date='div.update_time',
            chapter_image=''
        ),
        patterns=Patterns(
            index=r'[a-zA-Z\s]+([\d.]*):?[^.]*',
            upload_date=r'(\w{3})-(\d{2})-(\d{4})'
        )
    )

    def __init__(self, markup, parser='html.parser'):
        super().__init__(markup, self.SOURCE, parser)

    def parse_chapter_images(self, soup):
        selector = self.selector.chapter_image

        script_tags = soup.find_all(selector)
        script_string = ''
        for tag in script_tags:
            if 'var sv_checked' in str(tag) and 'var ytaw':
                script_string = str(tag)
                break

        if script_string:
            print('Searching script string')
            pattern = r'var ytaw\s?=\[(.+)\];'
            res = re.search(pattern, script_string)

            urls = []
            for string in res.groups()[0].split(','):
                string = string.replace('\'', '')
                if string:
                    urls.append(string)
