from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Advertiser(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=1000)
    img_url = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Action(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    user_ip = models.CharField(max_length=20)

    class Meta:
        abstract = True
    
class View(Action):
    pass
    # def __str__(self):
    #     return "Ad with id" + self.ad + "viewed at" + self.view_datetime

class Click(Action):
    pass
    # def __str__(self):
    #     return "Ad with id" + self.ad + "clicked at" + self.view_datetime
