from bs4 import BeautifulSoup
from wescrape.models.novel import Website, Status
from wescrape.parsers.nparse import NovelBaseParser, BoxNovelCom, WuxiaWorldCo


def identify_parser(url: str) -> NovelBaseParser:
    """Identifies `URL` and return required parser"""
    parser = None
    if Website.WUXIAWORLDCO.value in url:
        parser = WuxiaWorldCo()
    elif Website.BOXNOVELCOM.value in url:
        parser = BoxNovelCom()
    return parser


def identify_status(status: str) -> Status:
    """Identify string status, return corresponding Status object"""
    for key, val in enumerate(Status.__members__):
   
        if status.lower() == val.lower():
            status = Status(key)
            return status
    return Status.UPDATING


def parse_markup(markup: str, parser="html.parser") -> BeautifulSoup:
    soup = BeautifulSoup(markup, features=parser)
    return soup
    