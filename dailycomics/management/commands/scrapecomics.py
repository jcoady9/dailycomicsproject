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

    def scrape_dilbert_comic(self):
        DILBERT_URL = 'https://dilbert.com/'
        DILBERT_XPATH = 'body//img[@class=\'img-responsive img-comic\']'
        return self.generic_scrape(DILBERT_URL, DILBERT_XPATH)

    def scrape_baby_blues_comic(self):
        BABYBLUES_URL  = 'https://comicskingdom.com/baby-blues/'
        BABYBLUES_XPATH = '//body//slider-image'
        resp = requests.get(BABYBLUES_URL)
        if resp.status_code != 200:
            raise Exception('Unable to retrieve latest Baby Blues Comic Strip....')
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(resp.text), parser)
        src = tree.find(BABYBLUES_XPATH).get('image-url')
        return src

    def scrape_pearls_before_swine_comic(self):
        PEARLSBEFORESWINE_URL = 'https://www.gocomics.com/pearlsbeforeswine/'
        PEARLSBEFORESWINE_XPATH = 'body//picture[@class=\'item-comic-image\']/img'
        today = timezone.localtime().date()
        url = PEARLSBEFORESWINE_URL + today.strftime('%Y/%m/%d')
        return self.generic_scrape(url, PEARLSBEFORESWINE_XPATH)

    def scrape_bc_comic(self):
        BC_URL = 'https://www.gocomics.com/bc/'
        BC_XPATH = 'body//picture[@class=\'item-comic-image\']/img'
        today = timezone.localtime().date()
        url = BC_URL + today.strftime('%Y/%m/%d')
        return self.generic_scrape(url, BC_XPATH)

    def handle(self, *args, **options):
        comics = [
            ('Dilbert', self.scrape_dilbert_comic()),
            ('Baby Blues', self.scrape_baby_blues_comic()),
            ('Pearls Before Swine', self.scrape_pearls_before_swine_comic()),
            ('BC', self.scrape_bc_comic())
        ]
        for comic_strip in comics:
            ComicStrip(series_name=comic_strip[0], strip_url=comic_strip[1], date=timezone.localtime().date()).save()