from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('auth.User', related_name='advertisers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=1000)
    img_url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    advertiser = models.ForeignKey(Advertiser, related_name="ads", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class View(models.Model):
    ad = models.ForeignKey(Ad, related_name="views", on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    user_ip = models.CharField(max_length=20)


class Click(models.Model):
    ad = models.ForeignKey(Ad, related_name="clicks", on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    user_ip = models.CharField(max_length=20)

