from wescrape.models.novel import Selectors, Status, Website, Meta

class BaseParser:
    
    def __init__(self, selectors: Selectors):
        self.__selectors = selectors

    @staticmethod
    def identify(url):
        """Identifies `URL` where it comes from"""
        website = None
        if Website.WUXIAWORLDCO.value in url:
            website = Website.WUXIAWORLDCO
        elif Website.BOXNOVELCOM.value in url:
            website = Website.BOXNOVELCOM
        return website

    def parse_meta(self, soup: BeautifulSoup) -> Meta:
        title = self._parse_element_text(soup, self.__selectors.title)
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