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