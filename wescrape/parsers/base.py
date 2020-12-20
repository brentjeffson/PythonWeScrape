from bs4 import BeautifulSoup

class BaseParser():

    def __init__(self, markup, parser='html.parser'):
        self._markup = markup
        self._parser = parser
        self._links = []
        self._web_title = ''
        self._soup = None

        self.soup
    
    @property
    def web_title(self):
        if self._soup:
            if not self._web_title:
                self._web_title = self._soup.select_one('head > title').get_text()

        return self._web_title
    
    @property
    def links(self):
        if self._soup :
            if len(self._links) == 0:
                self._links = [ tag['href'] for tag in self._soup.select('a') ]

        return self._links

    @property
    def soup(self)
        if not self._soup:
            self._soup = BeautifulSoup(self._markup, self._parser)

        return self._soup
