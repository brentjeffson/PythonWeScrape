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