from wescrape.parsers.base import BaseParser
from wescrape.parsers.mparse import MangaParser, MANGA_SOURCES

from enum import Enum

class MediaType(Enum):
    MANGA = 0
    NOVEL = 1
    VIDEO = 2

class WeScrape:

    SOURCE_LIST = {
        MediaType.MANGA: MANGA_SOURCES,
    }

    @staticmethod
    def identify_media_type(html):
        base_parser = BaseParser(html)
        if base_parser.root_url in MANGA_SOURCES:
            return MediaType.MANGA
        if base_parser.root_url in NOVEL_SOURCES:
            return MediaType.NOVEL
        if base_parser.root_url in VIDEO_SOURCES:
            return MediaType.VIDEO

    @staticmethod
    def from_html(html, parser):
        media_type = WeScrape.identify_media_type(html)
        
        if media_type == MediaType.MANGA:
            parser = MangaParser(html, parser)
            return parser.parse_manga()
        
        if media_type == MediaType.NOVEL:
            # TODO
            pass
        
        if media_type == MediaType.VIDEO:
            # TODO YT
            pass