from enum import Enum
from typing import List
from dataclasses import dataclass, field

SPLITTERS = [';', ',', ':']


class MediaType(Enum):
    MANGA = 0
    # NOVEL = 1
    # VIDEO = 2


class Status(Enum):
    ONGOING = 0
    COMPLETED = 1
    HIATUS = 2
    UPDATING = 3


@dataclass
class Selectors:
    title: str
    chapter: str
    chapter_image: str
    thumbnail: str = ''
    alt_titles: str = ''
    authors: str = ''
    genres: str = ''
    rating: str = ''
    description: str = ''
    status: str = ''
    upload_date: str = ''


@dataclass
class Patterns:
    index: str = ''
    upload_date: str = ''


@dataclass
class Source:
    root_url: str
    image_base_url: str
    selectors: Selectors
    patterns: Patterns


@dataclass
class Info:
    alt_titles: List[str]
    authors: List[str]
    genres: List[str]
    rating: float
    description: str
    status: Status


@dataclass
class Chapter:
    url: str
    title: str
    index: int
    timestamp: float = 0
    content: str = ''
    image_urls: List = field(default_factory=list)


@dataclass
class Manga:
    url: str
    thumbnail_url: str
    title: str
    info: Info
    chapters: List[Chapter]

    def __len__(self):
        return len(self.chapters)