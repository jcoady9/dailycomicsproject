from django.core.management.base import BaseCommand
from django.utils import timezone

from io import StringIO
from urllib.parse import urlparse

from lxml import etree
import requests

from dailycomics.models import ComicStrip, Website, Series

class Command(BaseCommand):
    help = 'Scrapes internet for comic strips.'

    def generic_scrape(self, url, xpath):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception('Unable to retrieve latest comic...')
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(resp.text), parser)
        print(tree.find(xpath))
        src = tree.find(xpath).get('src')
        return src

    def gocomics_scrape(self, url):
        XPATH = 'body//picture[@class=\'item-comic-image\']/img'
        today = timezone.localtime().date()
        if url[-1] != '/':
            url = url + '/'
        print(url)
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
            comics.append(comic)

        ComicStrip.objects.bulk_create(comics)
