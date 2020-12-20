from pathlib import Path

from wescrape import WeScrape

if __name__ == '__main__':
    html_path = Path('tests', '__assets', 'markups', 'bug_player_home.html')
    html = html_path.read_bytes().decode()

    media_type = WeScrape.identify_media_type(html)
    media = WeScrape.from_html(html, 'html.parser')
    print(media_type.name.lower().capitalize())
    
    media.chapters.reverse()
    # chapters = '\n'.join([ f'[{chapter.index}] {chapter.title}: {chapter.url}' for chapter in manga.chapters ])