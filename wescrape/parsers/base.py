from bs4 import BeautifulSoup


class BaseParser():

    def __init__(self, markup, parser='html.parser'):
        self._markup = markup
        self._parser = parser
        self._soup = None
        self._web_url = ''
        self._web_title = ''
        self._links = []

    def _parse_web_url(self, soup):
        web_url = ''
        selectors = [
            'meta[property="og:url"]',
            'meta[name="og:url"]',
            'link[rel=canonical]'
        ]

        for selector in selectors:
            meta_url_tag = soup.select_one(selector)
            
            if meta_url_tag:
                attr = 'content' if 'meta' in selector else 'href'
                web_url = meta_url_tag[attr]
                break
        
        return web_url

    def _parse_web_title(self, soup):
        web_title = soup.select_one('head > title')
        return web_title if web_title else ''

    def _parse_web_links(self, soup):
        web_link_tags = soup.select('a')
        web_links = []
        if web_link_tags:
            web_links = [ tag['href'] for tag in web_link_tags ]
        return web_links if len(web_links) > 0 else None

    def load_markup(self, markup, parser='html.parser'):
        self._markup = markup
        self._parser = parser
        self._soup = self.soup
        self._web_url = self._parse_web_url(self._soup)
        self._web_title = self._parse_web_title(self._soup)

    def parse_item_list(self, soup, selector, splitter=';'):
        item_tags = soup.select(selector)
        items = []
        if item_tags and len(item_tags) == 1 and splitter:
            item_text = item_tags[0].get_text()
            item_parts = item_text.split(splitter)
            items = [item.strip() for item in item_parts]
        else:
            items = [item_tags.get_text() for item_tags in item_tags]
        return items

    @property
    def web_title(self):
        if self._web_title == '':
            self._web_title = self._parse_web_title(self.soup)
        return self._web_title

    @property
    def web_url(self):
        if self._web_url == '':
            self._web_url = self._parse_web_url(self.soup)
        return self._web_url

    @property
    def root_url(self):
        web_url = self.web_url
        if web_url:
            web_url_parts = web_url.split('/')
            if len(web_url_parts) >= 3:
                web_url = web_url_parts[2]
        return web_url

    @property
    def links(self):
        return self._links

    @property
    def soup(self):
        if self._soup is None or type(self._soup) != BeautifulSoup:
            self._soup = BeautifulSoup(self._markup, self._parser)
        return self._soup
