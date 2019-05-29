from django.urls import path

from .views import get_comics_for_day

urlpatterns = [
    path('', get_comics_for_day, name='comics-for-day'),
    path('<str:day>', get_comics_for_day, name='comics-for-day'),
]