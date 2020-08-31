from dataclasses import dataclass, field
from typing import List
from enum import Enum

class Website(Enum):
    BOXNOVELCOM = 'boxnovel.com'
    WUXIAWORLDCO = 'wuxiaworld.co'

class Status(Enum):
    ONGOING = 0
    COMPLETED = 1
    HIATUS = 2
    UPDATING = 3

@dataclass
class Entity:
    id: int
    title: str
    url: str

@dataclass
class Item:
    name: str
    value: str

@dataclass 
class Selector(Item):
    pass

@dataclass
class Selectors:
    title: str
    thumbnail: str
    chapters: str
    content: str
    authors: str
    genres: str
    description: str
    rating: str
    status: str
    release_date: str

@dataclass
class Author(Item):
    pass

@dataclass
class Genre(Item):
    pass

@dataclass
class Meta:
    authors: List[str] = field(default_factory=list)
    genres: List[str] = field(default_factory=list)
    rating: float = None
    release_date: str = None
    status: Status = None
    description: str = None

@dataclass
class Chapter(Entity):
    content: str = None

@dataclass
class Novel(Entity):
    thumbnail: str
    meta: Meta = None
    chapters: List[Chapter] = field(default_factory=list)