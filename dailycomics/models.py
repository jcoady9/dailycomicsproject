from django.db import models

# Create your models here.
class ComicStrip(models.Model):
    series_name = models.CharField(max_length=255)
    strip_url = models.CharField(max_length=255)
    date = models.DateField()

    class Meta:
        db_table = 'comicstrips'

class Website(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    xpath = models.CharField(max_length=255)

    class Meta:
        db_table = 'websites'

class Series(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'series'
