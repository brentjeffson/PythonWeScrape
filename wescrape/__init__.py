from wescrape.parsers.base import BaseParser
from wescrape.models.base import MediaType

from pathlib import Path
import importlib


class WeScrape:


    @staticmethod
    def identify_parser(html):
        class_ = None
        media_type = None
        root_url = BaseParser(html).root_url

        for media_type in MediaType:
            source_modules = []
            for path in Path('wescrape', 'parsers', media_type.name.lower()).iterdir():
                if not path.name.startswith('_') and path.is_file() and path.suffix == '.py':
                    source_modules.append(path.stem)

            if len(source_modules) == 0:
                break

            for source_module in source_modules:

                modules = importlib.import_module(
                    name=f'.{source_module}',
                    package=f'wescrape.parsers.{media_type.name.lower()}'
                )

                source_name = [d for d in dir(modules) if str(d).isupper()]
                if len(source_name) > 0:
                    source_name = getattr(modules, source_name[0])
                else:
                    source_name = source_module.capitalize()
                
                if source_name.lower() in root_url:
                    class_ = getattr(modules, source_name)
                    return class_, media_type
        return None, None

    @staticmethod
    def from_html(html, parser='html.parser'):
        class_, _ = WeScrape.identify_parser(html)
        if class_ is None:
            print('Unsupported website...')
            return None

        parser = class_(html, parser)
        return parser.parse()
