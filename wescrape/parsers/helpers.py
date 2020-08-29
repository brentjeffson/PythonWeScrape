from wescrape.models.novel import Website

def identify_parser(url):
    """Identifies `URL` where it comes from"""
    website = None
    if Website.WUXIAWORLDCO.value in url:
        website = Website.WUXIAWORLDCO
    elif Website.BOXNOVELCOM.value in url:
        website = Website.BOXNOVELCOM
    return website