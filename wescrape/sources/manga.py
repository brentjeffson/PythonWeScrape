from wescrape.models.manga import Selector, Pattern

MANGAKATANA = {
    'selectors': Selector(
        title = 'div.info > h1.heading',
        alt_titles = 'ul.meta > li:nth-child(1) > div:nth-child(2) > div.alt_name',
        authors = 'ul.meta > li:nth-child(2) > div:nth-child(2) > a',
        genres = 'ul.meta > li:nth-child(3) > div:nth-child(2) > div.genres > a',
        rating = '',
        description = 'div.summary > p',
        status = 'ul.meta > li:nth-child(4) > div:nth-child(2)',
        chapter = 'div.chapters div.chapter > a',
        upload_date = 'div.update_time'
    ),
    'patterns': Pattern(
        index = r'[a-zA-Z\s]+([\d.]*):?[^.]*',
        upload_date =  r'(\w{3})-(\d{2})-(\d{4})'
    )
}

FANFOX = {
    'selectors': Selector(
        title = 'div.detail-info p > span:nth-child(1)',
        alt_titles = '',
        authors = 'p.detail-info-right-say > a',
        genres = 'p.detail-info-right-tag-list > a',
        rating = 'div.detail-info p > span:nth-child(3) > span.item-score',
        description = 'p.detail-info-right-content',
        status = 'div.detail-info p > span:nth-child(2)',
        chapter = 'div#chapterlist li > a',
        upload_date = 'div#chapterlist li > a p:nth-child(2)'
    ),
    'patterns': Pattern(
        index = r'[a-zA-Z.\s1-9]+[\s.]?[a-zA-Z]+[\s.]?([\d.]+)\s?\-?\s?[\w\d]+',
        upload_date =  r'(\w{3})\s?(\d{2}),?\s?(\d{4})'
    )
}