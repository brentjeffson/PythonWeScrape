from wescrape.models.novel import Status
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


def identify_status(status: str) -> Status:
    """Identify string status, return corresponding Status object"""
    if status == Status.ONGOING.name.lower():
        status = Status.ONGOING
    elif status == Status.COMPLETED.name.lower():
        status = Status.COMPLETED
    elif status == Status.HIATUS.name.lower():
        status = Status.HIATUS
    else:
        status = Status.UPDATING
    return status