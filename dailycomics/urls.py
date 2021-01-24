from django.urls import path

from .views import get_comics_for_day, scrape_comics

urlpatterns = [
    path('', get_comics_for_day, name='comics-for-day'),
    path('<str:day>', get_comics_for_day, name='comics-for-day'),
    path('/scrape', scrape_comics, name='scrape-comics'),
]