from django.shortcuts import render

from .models import Advertiser, Ad


# Create your views here.

def new_ad(request):
    return(render(request, "advertiser_management/new_ad.html"))

def ads(request):
    if(request.method == "POST"):
        pass
    else:
        advertisers = Advertiser.objects.all()
        return(render(request, "advertiser_management/ads.html", {"advertisers": advertisers}))