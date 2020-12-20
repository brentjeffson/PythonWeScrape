import re
import datetime

from wescrape.parsers.base import BaseParser
from wescrape.models.manga import Status, Info, Chapter, Manga
from wescrape.sources.manga import MANGAKATANA

MANGA_SOURCES = {
    'mangakatana.com': MANGAKATANA
}

class MangaParser(BaseParser):

    def __init__(self, markup, parser):
        super().__init__(markup, parser)

        self._selector = None
        self._pattern = None

        if super().root_url in MANGA_SOURCES:
            self._selector = MANGA_SOURCES[super().root_url]['selectors']
            self._pattern = MANGA_SOURCES[super().root_url]['patterns']
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
                        
                        month = months.index(month) + 1 if type(month) == str else month
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
                index = index_res.groups()[0]
                index = float(index)
            
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
