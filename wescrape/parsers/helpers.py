from wescrape.models.novel import Website
from wescrape.parsers.nparse import BoxNovelCom, WuxiaWorldCo

def identify_parser(url):
    """Identifies `URL` and return required parser"""
    parser = None
    if Website.WUXIAWORLDCO.value in url:
        parser = WuxiaWorldCo()
    elif Website.BOXNOVELCOM.value in url:
        parser = BoxNovelCom()
    return parser