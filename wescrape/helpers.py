from bs4 import BeautifulSoup
from wescrape.models.novel import Website, Status, Novel
from wescrape.parsers.nparse import NovelBaseParser, BoxNovelCom, WuxiaWorldCo
import requests


def identify_parser(url: str) -> NovelBaseParser:
    """Identifies `URL` And Return Required Parser"""
    parser = None
    if Website.WUXIAWORLDCO.value in url:
        parser = WuxiaWorldCo()
    elif Website.BOXNOVELCOM.value in url:
        parser = BoxNovelCom()
    return parser


def identify_status(status: str) -> Status:
    """Identify String Status, Return Corresponding Status object"""
    for key, val in enumerate(Status.__members__):
   
        if status.lower() == val.lower():
            status = Status(key)
            return status
    return Status.UPDATING


def parse_markup(markup: str, parser="html.parser") -> BeautifulSoup:
    soup = BeautifulSoup(markup, features=parser)
    return soup


def search(session: requests.Session, keyword: str, website: Website) -> [Novel]:
    novels = []
    if website == Website.BOXNOVELCOM:
        payload = {
            "action": "wp-manga-search-manga",
            "title": self.search_input.text
        }
        resp = session.post("https://boxnovel.com/wp-admin/admin-ajax.php", data=payload)
        if resp.ok:
            for novel in resp.json()["data"]:
                novels.append(Novel(
                    id=novel["url"],
                    title=novel["title"],
                    url=novel["url"],
                    thumbnail=""
                ))
    elif website == Website.WUXIAWORLDCO:
        search_selector = "ul.result-list > li.list-item > a.list-img"
        keyword = keyword.replace(" ", "%20")
        endpoint = '/'.join(["https://m.wuxiaworld.co/search", keyword, "1"])
        resp = session.get(endpoint)
        if resp.ok:
            markup = resp.text
            soup = parse_markup(markup)
            novel_tags = soup.select(search_selector)
            for tag in novel_tags:
                img_tag = tag.find("img")
                url = ''.join(["https://m.wuxiaworld.co", tag["href"]])
                title = img_tag["alt"]

                novels.append(Novel(
                    id=url,
                    title=title,
                    url=url,
                    thumbnail=""
                ))
    return novels