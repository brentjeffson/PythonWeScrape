import re
import datetime

from wescrape.parsers.base import BaseParser
from wescrape.models.base import Status, Info, Chapter, Manga


class MangaParser(BaseParser):

    def __init__(self, markup, source, parser):
        super().__init__(markup, parser)

        if self.root_url not in source.root_url:
            print('Unable to parse markup.')

        self._selector = source.selectors
        self._pattern = source.patterns
    
    @staticmethod
    def split_selector(selector, splitter='::'):
        parts = selector.split(splitter)
        if len(parts) > 1:
            splitter = parts[0]
            selector = parts[1]
        else:
            splitter=''
        return selector, splitter

    def _parse_elements(self, soup, selector, splitter=''):
        selector, splitter = self.split_selector(selector)
        elements = super().parse_item_list(soup, selector, splitter)
        elements = [ element.strip() for element in elements ]
        return elements
    
    def _parse_thumbnail(self, soup, selector):
        thumbnail_tag = soup.select_one(selector)
        if thumbnail_tag.name == 'img':
            return thumbnail_tag['src']
        return None

    def _parse_title(self, soup, selector):
        title_tag = soup.select_one(selector)
        return title_tag.get_text().strip() if title_tag else ''

    def _parse_alt_titles(self, soup, selector, splitter=''):
        return self._parse_elements(soup, selector, splitter)

    def _parse_authors(self, soup, selector, splitter=''):
        return self._parse_elements(soup, selector, splitter)

    def _parse_genres(self, soup, selector, splitter=''):
        return self._parse_elements(soup, selector, splitter)

    def _parse_rating(self, soup, selector):
        rating_tag = None
        if selector:
            rating_tag = soup.select_one(selector)
        return rating_tag.get_text().strip() if rating_tag else -1

    def _parse_description(self, soup, selector, splitter=''):
        description = super().parse_item_list(soup, selector, splitter)
        if type(description) == list and len(description) > 1:
            description = '\n'.join(description)
        else:
            description = ''
        return description.strip()

    def _parse_status(self, soup, selector):
        status_tag = soup.select_one(selector)
        status = status_tag.get_text() if status_tag else ''
        for s in Status:
            if status == s.value:
                status = s
                break
        return status.strip()

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

    def _parse_info(self, soup, alt_titles_sel, authors_sel, genres_sel, 
        rating_sel, description_sel, status_sel):

        alt_titles, authors, genres, rating, description, status = [''] * 6

        if alt_titles_sel:
            alt_titles = self._parse_alt_titles(soup, alt_titles_sel)
        if authors_sel:
            authors = self._parse_authors(soup, authors_sel)
        if genres_sel:
            genres = self._parse_genres(soup, genres_sel)
        if rating_sel:
            rating = self._parse_rating(soup, rating_sel)
        if description_sel:
            description = self._parse_description(soup, description_sel)
        if status_sel:
            status = self._parse_status(soup, status_sel)

        return Info(
            alt_titles=alt_titles,
            authors=authors,
            genres=genres,
            rating=rating,
            description=description,
            status=status
        )

    def _parse_chapters(self, soup, chapter_sel, upload_date_sel, 
        index_pattern, upload_date_pattern):

        chapter_tags = soup.select(chapter_sel)

        upload_dates = self._parse_chapter_timestamps(
            soup,
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

    def parse(self):
        url = self.web_url
        thumbnail = ''
        if self.selector.thumbnail:
            thumbnail = self._parse_thumbnail(super().soup, self.selector.thumbnail)
        title = self._parse_title(super().soup, self.selector.title)
        info = self._parse_info( 
            super().soup,
            self.selector.alt_titles,
            self.selector.authors,
            self.selector.genres,
            self.selector.rating,
            self.selector.description,
            self.selector.status
        )
        chapters = self._parse_chapters(
            super().soup,
            self.selector.chapter,
            self.selector.upload_date,
            index_pattern=self.pattern.index,
            upload_date_pattern=self.pattern.upload_date
        )
        return Manga(url=url, thumbnail_url=thumbnail, title=title, info=info, chapters=chapters) 

    def parse_chapter_images(self, markup):
        soup = BaseParser(markup).soup
        img_urls = []
        chapter_tags = soup.select(self.selector.chapter_image)
        if chapter_tags:
            for tag in chapter_tags:
                if tag.name == 'img':
                    img_urls.append(tag['src'])

        return img_urls

    @property
    def selector(self):
        return self._selector

    @property
    def pattern(self):
        return self._pattern
