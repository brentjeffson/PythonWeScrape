import re
import datetime
from wescrape.parsers.base import BaseParser
from enum import Enum
from dataclasses import dataclass, field
from typing import List


class Status(Enum):
    ONGOING = 0
    COMPLETED = 1
    HIATUS = 2
    UPDATING = 3


@dataclass
class Selector:
    title: str
    alt_titles: str
    authors: str
    genres: str
    rating: str
    description: str
    status: str
    chapter: str
    upload_date: str


@dataclass
class Pattern:
    index: str
    upload_date: str


@dataclass
class Info:
    alt_titles: List[str]
    authors: List[str]
    genres: List[str]
    rating: float
    description: str
    status: Status


@dataclass
class Chapter:
    url: str
    title: str
    index: int
    timestamp: float = 0
    content: str = ''


@dataclass
class Manga:
    url: str
    title: str
    info: Info
    chapters: List[Chapter]

    def __len__(self):
        return len(self.chapters)

    @classmethod
    def from_html(cls, markup):
        parser = MangaParser(markup, 'html.parser')
        return parser.parse_manga()


MANGAKATANA = {
    'selectors': Selector(
        title = 'div.info > h1.heading',
        alt_titles = 'ul.meta > li:nth-child(1) > div:nth-child(2) > div.alt_name',
        authors = 'ul.meta > li:nth-child(2) > div:nth-child(2) > a',
        genres = 'ul.meta > li:nth-child(3) > div:nth-child(2) > div.genres > a',
        rating = '',
        description = 'div.summary > p',
        status = 'ul.meta > li:nth-child(4) > div:nth-child(2)',
        chapter = 'div.chapters div.chapter > a',
        upload_date = 'div.update_time'
    ),
    'patterns': Pattern(
        index = r'[a-zA-Z\s]+([\d.]*):?[^.]*',
        upload_date =  r'(\w{3})-(\d{2})-(\d{4})'
    )
}

SOURCES = {
    'mangakatana.com': MANGAKATANA
}

class MangaParser(BaseParser):

    def __init__(self, markup, parser):
        super().__init__(markup, parser)

        self._selector = None
        self._pattern = None

        if super().root_url in SOURCES:
            self._selector = SOURCES[super().root_url]['selectors']
            self._pattern = SOURCES[super().root_url]['patterns']
        else:
            print(f'Unsupported source {super().root_url}')

    def _parse_title(self, soup, selector):
        title_tag = soup.select_one(selector)
        return title_tag.get_text() if title_tag else ''

    def _parse_alt_titles(self, soup, selector, splitter=''):
        alt_titles = super().parse_item_list(soup, selector, splitter)
        return alt_titles
    
    def _parse_authors(self, soup, selector, splitter=''):
        authors = super().parse_item_list(soup, selector, splitter)
        return authors
    
    def _parse_genres(self, soup, selector, splitter=''):
        genres = super().parse_item_list(soup, selector, splitter)
        return genres

    def _parse_rating(self, soup, selector):
        rating_tag = None
        if selector:
            rating_tag = soup.select_one(selector)
        return rating_tag.get_text() if rating_tag else -1

    def _parse_description(self, soup, selector, splitter=''):
        description = super().parse_item_list(soup, selector, splitter)
        if type(description) == list and len(description) > 1:
            description = '\n'.join(description)
        return description
    
    def _parse_status(self, soup, selector):
        status_tag = soup.select_one(selector)
        status = status_tag.get_text() if status_tag else None
        for s in Status:
            if status == s.value:
                status = s
                break
        return status

    def _parse_chapter_timestamps(self, soup, upload_date_sel, upload_date_pattern):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        upload_dates = []
        if upload_date_sel:
            upload_tags = soup.select(upload_date_sel)
            if upload_tags:
                for upload_tag in upload_tags:
                    timestamp = 0
                    upload_date = upload_tag.get_text()
                    res = re.search(upload_date_pattern, upload_date)
                    
                    if res and len(res.groups()) == 3:
                        if len(str(res.groups()[2])) == 4:
                            month, day, year = res.groups()
                        elif len(str(res.groups()[0])) == 4:
                            year, month, day = res.groups()
                        
                        month = month.index(month) + 1 if type(month) == str else month
                        month = month[1:] if type(month) == str and month.startswith('0') else month
                        day = day[1:] if type(day) == str and day.startswith('0') else day

                        timestamp = datetime.datetime(int(year), int(month), int(day)).timestamp()
                    upload_dates.append(timestamp)
        return upload_dates

    def _parse_info(self, alt_titles_sel, authors_sel, genres_sel, 
        rating_sel, description_sel, status_sel):

        alt_titles = self._parse_alt_titles(self.soup, alt_titles_sel, ';')
        authors = self._parse_authors(self.soup, authors_sel)
        genres = self._parse_genres(self.soup, genres_sel)
        rating = self._parse_rating(self.soup, rating_sel)
        description = self._parse_description(self.soup, description_sel)
        status = self._parse_status(self.soup, status_sel)

        return Info(
            alt_titles = alt_titles,
            authors = authors,
            genres = genres,
            rating = rating,
            description = description,
            status = status
        )

    def _parse_chapters(self, chapter_sel, upload_date_sel, index_pattern, upload_date_pattern):
        chapter_tags = super().soup.select(chapter_sel)

        upload_dates = self._parse_chapter_timestamps(
            super().soup,
            upload_date_sel,
            upload_date_pattern
        )
        
        chapters = []
        for idx, chapter_tag in enumerate(chapter_tags):
            url = chapter_tag['href']
            title = chapter_tag.get_text()
            index_res = re.search(index_pattern, title)
            if index_res:
                index = index_res.groups(1)
            
            upload_date = 0
            if upload_dates and len(upload_dates) == len(chapter_tags):
                upload_date = upload_dates[idx]

            chapters.append(Chapter(url, title, index, upload_date))
        return chapters

    def parse_manga(self):

        url = self.web_url
        title = self._parse_title(super().soup, self._selector.title)
        info = self._parse_info( 
            self._selector.alt_titles, 
            self._selector.authors, 
            self._selector.genres, 
            self._selector.rating, 
            self._selector.description, 
            self._selector.status
        )
        chapters = self._parse_chapters(
            self._selector.chapter,
            self._selector.upload_date,
            index_pattern = self._pattern.index,
            upload_date_pattern = self._pattern.upload_date
        )
        
        return Manga(url, title, info, chapters)
