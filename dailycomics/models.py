from django.db import models

# Create your models here.
class ComicStrip(models.Model):
    series_name = models.CharField(max_length=255)
    strip_url = models.CharField(max_length=255)
    date = models.DateField()