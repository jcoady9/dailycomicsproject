from django.core.management.base import BaseCommand
from django.utils import timezone

from io import StringIO
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

from dailycomics.models import ComicStrip, Website, Series

class Command(BaseCommand):
    help = 'Scrapes internet for comic strips.'

    def generic_scrape(self, url, css_selector):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception('Unable to retrieve latest comic...')
        soup = BeautifulSoup(resp.text, 'html.parser')
        src = soup.select_one(css_selector).get('src')
        return src

    def gocomics_scrape(self, url):
        XPATH = 'body//picture[@class=\'item-comic-image\']/img'
        CSS_SELECTOR = '.item-comic-image > img:nth-child(1)'
        today = timezone.localtime().date()
        if url[-1] != '/':
            url = url + '/'
        return self.generic_scrape(''.join([url, today.strftime('%Y/%m/%d')]), CSS_SELECTOR)

    def comicskingdom_scrape(self, url):
        XPATH = '//body//slider-image'
        CSS_SELECTOR = 'slider-image'
        
        resp = requests.get(url,verify=False)
        if resp.status_code != 200:
            raise Exception('Unable to retrieve latest Baby Blues Comic Strip....')
        soup = BeautifulSoup(resp.text, 'html.parser')
        src = soup.select_one(CSS_SELECTOR).get('image-url')
        return src

    def scrape_dilbert_comic(self):
        DILBERT_URL = 'https://dilbert.com/'
        DILBERT_XPATH = 'body//img[@class=\'img-responsive img-comic\']'
        DILBERT_CSS_SELECTOR = 'div.comic-item-container:nth-child(2) > div:nth-child(1) > section:nth-child(1) > div:nth-child(4) > a:nth-child(1) > img:nth-child(1)'
        return self.generic_scrape(DILBERT_URL, DILBERT_CSS_SELECTOR)

    def handle(self, *args, **options):
        series_list = Series.objects.all()

        comics = []
        for series in series_list:
            o = urlparse(series.url)
            strip_url = ''
            if 'dilbert' in o.hostname:
                strip_url = self.scrape_dilbert_comic()
            if  'gocomics' in o.hostname:
                strip_url = self.gocomics_scrape(series.url)
            if 'comicskingdom' in o.hostname:
                strip_url = self.comicskingdom_scrape(series.url)
            
            comic = ComicStrip(series_name=series.name, strip_url=strip_url, date=timezone.localtime().date())
            print('{} - {}'.format(comic.series_name, comic.strip_url))
            comics.append(comic)

        ComicStrip.objects.bulk_create(comics)
