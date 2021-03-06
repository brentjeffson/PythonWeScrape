from bs4 import BeautifulSoup
import re
import json


    
class YoutubeParser:

    @staticmethod
    def parse_sources(markup, parser='html.parser'):

        def clean(format_text):
            """Clean raw source"""
            while True:
                res = re.search(r'"mimeType":"([\w/]+); codecs=("[\w.,\s]+")","bitrate"', format_text)
                if res is None:
                    break
                format_text = format_text.replace(res.groups()[1], res.groups()[1].replace("\"", ""))
            return format_text

        # find script containing video informations
        soup = BeautifulSoup(markup, parser)
        player_script_tag = soup.select("div#player script:nth-of-type(2)")
        text = player_script_tag[0].string

        # search string containing youtube sources
        searched_format = re.search(r'\\"formats\\":.+,\\"adaptiveFormats\\":', text)
        searched_adaptive_format = re.search(r',\\"adaptiveFormats\\":.+},\\"playerAds\\":', text)

        # get formats
        format_sources = text[searched_format.start():searched_format.end()] \
            .replace(',\\"adaptiveFormats\\":', '') \
            .replace('\\"formats\\":', '') \
            .replace('\\', '').replace('u0026', '&')
        adaptive_format_sources = text[searched_adaptive_format.start():searched_adaptive_format.end()] \
            .replace(',\\"adaptiveFormats\\":', "") \
            .replace('},\\"playerAds\\":', "") \
            .replace('\\', '').replace('u0026', '&')

        # clean formats
        format_sources = clean(format_sources)
        adaptive_format_sources = clean(adaptive_format_sources)

        # check if formats are valid
        sources = []
        try:           
            sources.extend(json.loads(format_sources))
            sources.extend(json.loads(adaptive_format_sources))
        except Exception as ex:
            print(ex)
            print('Error: Invalid Format')
        finally:
            return sources

    @staticmethod
    def classify_sources(sources):
            """Classifies sources"""
            categories = {
                'video': [],
                'audio': [],
                'video_audio': [],
                'uncategorized': []
            }
            for s in sources:
                mime = s['mimeType']
                split_mime = mime.split(';')
                
                if len(split_mime[1].split(',')) > 1:
                    categories['video_audio'].append(s)
                elif 'video' in mime:
                    categories['video'].append(s)
                elif 'audio' in mime:
                    categories['audio'].append(s)
                else:
                    categories['uncategorized'].append(s)
            return categories

    @staticmethod
    def list_sources(sources):
        categories = YoutubeParser.classify_sources(sources)

        for category in categories:
            header = '{:^8} {:^13} {:^14} {:^12} {:^12} {:^9}'.format('CODE', 'EXTENSION', 'RESOLUTION', 'SIZE', 'BITRATE', 'CODEC')
            padding = int( ( len( header ) - len( category ) ) / 2 )
            
            print(f'{ "="*padding } { category.upper() } { "="*padding }')
            print(header)
            
            for source in categories[category]:

                tag = source['itag']
                extension = source['mimeType'].split(';')[0].split('/')[1]
                resolution = source['qualityLabel'] if 'qualityLabel' in source.keys() else source['quality']
                size = float(source['contentLength']) / 1024 / 1024 if 'contentLength' in source.keys() else 0.0
                bitrate = int(source['bitrate']) / 1000
                codec = source['mimeType'].split(';')[1].split('=')[1]
                
                formated_string = '{tag:^8} {extension:^13} {resolution:^14} {size:^12} {bitrate:^12} {codec:^9}'.format(
                    tag=tag, 
                    extension=extension, 
                    resolution=resolution, 
                    size='{:.2f} MB'.format(size), 
                    bitrate='{:.0f}K'.format(bitrate), 
                    codec=codec
                )
                print(formated_string)
        




