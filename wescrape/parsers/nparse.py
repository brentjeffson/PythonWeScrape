from wescrape.models.novel import Selectors, Status, Meta, Chapter
from typing import List
from bs4 import BeautifulSoup

class BaseParser:
    
    def __init__(self, selectors: Selectors):
        self.__selectors = selectors
    
    def parse_title(self, soup: BeautifulSoup) -> str:
        title = self._parse_element_text(soup, self.__selectors.title)
        title = title.replace('\n', '').replace('\r', '').replace('\t', '').strip()
        return title

    def parse_meta(self, soup: BeautifulSoup) -> Meta:
        authors = self._parse_list_element_text(soup, self.__selectors.authors)
        genres = self._parse_list_element_text(soup, self.__selectors.genres)
        description = self._parse_element_text(soup, self.__selectors.description)
        rating = float(self._parse_element_text(soup, self.__selectors.rating))
        release_date = self._parse_element_text(soup, self.__selectors.release_date)
        status = self._parse_element_text(soup, self.__selectors.status).lower()
        if status == Status.ONGOING.name.lower():
            status = Status.ONGOING
        elif status == Status.COMPLETED.name.lower():
            status = Status.COMPLETED
        else:
            status = Status.HIATUS
        return Meta(
            authors=authors,
            genres=genres,
            rating=rating,
            release_date=release_data,
            status=status
        )

    def _parse_element_text(self, soup, selector) -> str:
        element = soup.select_one(selector)
        return element.text

    def _parse_list_element_text(self, soup, selector) -> List:
        elements = soup.select(selector)
        items = []
        for element in elements:
            items.append(element.text)
        return items

    def parse_chapters(self, soup: BeautifulSoup) -> List[Chapter]:
        chapter_elements = soup.select(self.__selectors.chapters)
        chapters = []
        for element in chapter_elements:
            chapter_title = element.text
            chapter_id = re.findall('([\d\.]+)', chapter_title)[0]
            chapter_url = element['href']
            chapters.append(Chapter(
                id=int(chapter_id), 
                title=chapter_title, 
                url=chapter_url
            ))
        return chapters

    def parse_content(self, soup: BeautifulSoup) -> str:
        return '\n'.join(self._parse_list_element_text(soup, self.__selectors.content))

class WuxiaWorldCo(BaseParser):
    SELECTORS = Selectors(
        title='div.book-info > div.book-name',
        chapters='a.chapter-item', 
        content='div.chapter-entity',
        authors='div.author > span.name', 
        genres='div.book-catalog > span.txt',
        description='div.content > p.desc', 
        rating='span.score', 
        status='div.book-state > span.txt',
        release_date=''
    )

    def __init__(self):
        super(WuxiaWorldCo, self).__init__(self.SELECTORS)

    def parse_chapters(self, soup: BeautifulSoup) -> List:
        chapters = super().parse_chapters(soup)
        # reverse order from descending to ascending
        chapters = chapters[::-1]
        return chapters

    def parse_content(self, soup: BeautifulSoup) -> str:
        content_element = soup.select_one(self.SELECTORS.content)
        content = content_element.text\
            .replace('(adsbygoogle = window.adsbygoogle || []).push({});', '') \
            .replace('\r\n', '').replace('  ', '').replace('\n\n\n', '').replace('\n\n\n\n', '')
            # .replace('\r\n', '').replace(' ' * 24, '').replace('<br/>', '\n')

        return content
    
class BoxNovelCom(BaseParser):
    SELECTORS = Selectors(
        title='ol.breadcrumb > li:last-child',
        chapters='li.wp-manga-chapter > a', 
        content='div.cha-words p ::: div.text-left > p',
        authors='div.author-content > a', 
        genres='div.genres-content',
        description='div#editdescription', 
        rating='div.post-total-rating > span.total_votes',
        status='div.post-status > div:nth-child(2) > div:last-child',
        release_date='div.post-status > div:nth-child(1) > div:last-child'
    )

    def __init__(self):
        super(BoxNovelCom, self).__init__(self.SELECTORS)

    def parse_meta(self, soup: BeautifulSoup) -> Meta:
        meta =  super().parse_meta(soup)
        meta.genres = [genre.replace('\n', '') for genre in meta.genres]
        meta.authors = [author.replace('\n', '') for author in meta.authors]
        meta.description = meta.description[1:]
        return meta

    def parse_chapters(self, soup: BeautifulSoup) -> List[Chapter]:
        chapters = super().parse_chapters(soup)
        for chapter in chapters:
            chapter.title = chapter.title.replace('\t', '').replace('\n', '').strip()
        return chapters

    def parse_content(self, soup: BeautifulSoup) -> str:
        paragraph_elements = soup.select(self.SELECTORS.content.split(':::')[0].strip())
        if len(paragraph_elements) == 0:
            paragraph_elements = soup.select(self.SELECTORS.content.split(':::')[1].strip())
        content_list = [element.text for element in paragraph_elements]
        return '\n\n'.join(content_list)
