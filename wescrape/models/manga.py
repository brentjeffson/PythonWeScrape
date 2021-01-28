from enum import Enum
from typing import List
from dataclasses import dataclass


class Status(Enum):
    ONGOING = 0
    COMPLETED = 1
    HIATUS = 2
    UPDATING = 3


@dataclass
class Selector:
    thumbnail: str
    title: str
    alt_titles: str
    authors: str
    genres: str
    rating: str
    description: str
    status: str
    chapter: str
    upload_date: str


@dataclass
class Pattern:
    index: str
    upload_date: str


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


@dataclass
class Manga:
    url: str
    thumbnail_url: str
    title: str
    info: Info
    chapters: List[Chapter]

    def __len__(self):
        return len(self.chapters)