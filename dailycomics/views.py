from datetime import date

from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView

from .models import ComicStrip

# Create your views here.
# def get_comics_for_day(req, day=date.today().isoformat()):
def get_comics_for_day(req, day=timezone.localtime().date().isoformat()):
    day = date.fromisoformat(day)
    previous_day = day.replace(day=day.day - 1)
    next_day = day.replace(day=day.day + 1)
    queryset = ComicStrip.objects.filter(date=day)
    return render(req, 'dailycomics/daily_comics_list.html', { 'comics' : queryset, 'chosen_day' : day, 'previous_day' : previous_day, 'next_day' : next_day })
