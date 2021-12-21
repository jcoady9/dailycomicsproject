from datetime import date, timedelta

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from .models import ComicStrip

from .management.commands.scrapecomics import Command

DAY_DELTA = timedelta(hours=24)

# Create your views here.
def get_comics_for_day(req, day=None):
    if day == None:
        day = timezone.localtime().date().isoformat()
    day = date.fromisoformat(day)
    previous_day = day - DAY_DELTA
    next_day = day + DAY_DELTA
    queryset = ComicStrip.objects.filter(date=day)
    return render(req, 'dailycomics/daily_comics_list.html', { 'comics' : queryset, 'chosen_day' : day, 'previous_day' : previous_day, 'next_day' : next_day })

def scrape_comics(req):

    if req.method == 'POST':
        cmd = Command()
        cmd.handle()
        return HttpResponseRedirect('{}'.format(timezone.localtime().date().isoformat()))
