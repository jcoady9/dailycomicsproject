from django.core.management.base import BaseCommand
from django.utils import timezone

from io import StringIO

from lxml import etree
import requests

from dailycomics.models import ComicStrip

class Command(BaseCommand):
    help = 'Scrapes internet for comic strips.'

    def generic_scrape(self, url, xpath):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception('Unable to retrieve latest comic...')
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(resp.text), parser)
        src = tree.find(xpath).get('src')
        return src

    def gocomics_scrape(self, url):
        XPATH = 'body//picture[@class=\'item-comic-image\']/img'
        today = timezone.localtime().date()
        if url[-1] != '/':
            url = url + '/'
        return self.generic_scrape(''.join([url, today.strftime('%Y/%m/%d')]), XPATH)

    def comicskingdom_scrape(self, url):
        XPATH = '//body//slider-image'
        resp = requests.get(url,verify=False)
        if resp.status_code != 200:
            raise Exception('Unable to retrieve latest Baby Blues Comic Strip....')
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(resp.text), parser)
        src = tree.find(XPATH).get('image-url')
        return src

    def scrape_dilbert_comic(self):
        DILBERT_URL = 'https://dilbert.com/'
        DILBERT_XPATH = 'body//img[@class=\'img-responsive img-comic\']'
        return self.generic_scrape(DILBERT_URL, DILBERT_XPATH)

    def scrape_baby_blues_comic(self):
        BABYBLUES_URL  = 'https://comicskingdom.com/baby-blues/'
        return self.comicskingdom_scrape(BABYBLUES_URL)

    def scrape_pearls_before_swine_comic(self):
        PEARLSBEFORESWINE_URL = 'https://www.gocomics.com/pearlsbeforeswine/'
        return self.gocomics_scrape(PEARLSBEFORESWINE_URL)

    def scrape_bc_comic(self):
        BC_URL = 'https://www.gocomics.com/bc/'
        return self.gocomics_scrape(BC_URL)

    def scrape_non_sequitur(self):
        NON_SEQUITUR_URL = 'https://www.gocomics.com/nonsequitur/'
        return self.gocomics_scrape(NON_SEQUITUR_URL)

    def scrape_doonesbury(self):
        DOONESBURY_URL = 'https://www.gocomics.com/doonesbury/'
        return self.gocomics_scrape(DOONESBURY_URL)

    def scrape_zits(self):
        ZITS_URL  = 'https://comicskingdom.com/zits/'
        return self.comicskingdom_scrape(ZITS_URL)

    def handle(self, *args, **options):
        comics = []
        try:
            comics.append(('Dilbert', self.scrape_dilbert_comic()))
        except Exception as e:
            print('failed to scrape Dilbert... {}'.format(e))

        try:
            comics.append(('Baby Blues', self.scrape_baby_blues_comic()))
        except Exception as e:
            print('Failed to scrape Baby Blues... {}'.format(e))

        try:
            comics.append(('Pearls Before Swine', self.scrape_pearls_before_swine_comic()))
        except Exception as e:
            print('Failed to scrape Pearls Before Swine... {}'.format(e))

        try:
            comics.append(('BC', self.scrape_bc_comic()))
        except Exception as e:
            print('Failed to scrape BC... {}'.format(e))

        try:
            comics.append(('Non Sequitur', self.scrape_non_sequitur()))
        except Exception as e:
            print('Failed to scrape Non Sequitur... {}'.format(e))

        try:
            comics.append(('Doonesbury', self.scrape_doonesbury()))
        except Exception as e:
            print('Failed to scrape Doonesbury... {}'.format(e))

        try:
            comics.append(('Zits', self.scrape_zits()))
        except Exception as e:
            print('Failed to scrape Doonesbury... {}'.format(e))

        for comic_strip in comics:
            ComicStrip(series_name=comic_strip[0], strip_url=comic_strip[1], date=timezone.localtime().date()).save()
