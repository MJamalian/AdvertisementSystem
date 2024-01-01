from django.db import models

# Create your models here.


class BaseAdvertising(models.Model):
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)


    class Meta:
        abstract = True

class Advertiser(BaseAdvertising):
    name = models.CharField(max_length=50)


class Ad(BaseAdvertising):
    title = models.CharField(max_length=1000)
    img_url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
