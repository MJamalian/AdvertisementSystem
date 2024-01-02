from django.shortcuts import render

from .models import Advertiser, Ad
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def new_ad(request):
    return(render(request, "advertiser_management/create_ad.html"))

def ads(request):

    def show_ads():
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ad_set.all():
                ad.views += 1
                advertiser.views += 1
                ad.save()
            advertiser.save()
        return(render(request, "advertiser_management/ads.html", {"advertisers": advertisers}))

    if(request.method == "POST"):
        advertiser_id = request.POST["advertiser_id"]
        try:
            advertiser = Advertiser.objects.get(pk=advertiser_id)
        except ObjectDoesNotExist:
            return(render(request, "advertiser_management/create_ad.html", {"error_message": "Advertiser with that id doesn't exist."}))
        else:
            advertiser.ad_set.create(title=request.POST["title"], img_url=request.POST["img_url"], link=request.POST["link"])
            return(show_ads())
    elif(request.method == "GET"):
        return(show_ads())