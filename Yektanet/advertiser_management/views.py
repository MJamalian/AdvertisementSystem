from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse

from .models import Advertiser, Ad
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.list import ListView

# Create your views here.

    
class AdCreateView(TemplateView):
    template_name = "advertiser_management/create_ad.html"

    def post(self, request, *args, **kwargs):
        advertiser_id = request.POST["advertiser_id"]
        try:
            advertiser = Advertiser.objects.get(pk=advertiser_id)

        except ObjectDoesNotExist:
            return(render(request, self.template_name, {"error_message": "Advertiser with that id doesn't exist."}))
        
        else:
            advertiser.ad_set.create(title=request.POST["title"], img_url=request.POST["img_url"], link=request.POST["link"])
            return HttpResponseRedirect(reverse("advertiser_management:show_ads"))

class AdShowView(ListView):
    model = Advertiser
    context_object_name = "advertisers"
    template_name = "advertiser_management/ads.html"

    def get(self, request, *args, **kwargs):
        for ad in Ad.objects.all():
            if(ad.approved):
                ad.view_set.create(user_ip=request.user_ip)

        return super().get(self, request, *args, **kwargs)
    
class AdRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs["ad_id"])
        ad.click_set.create(user_ip=self.request.user_ip)
        self.url = ad.link
        return super().get_redirect_url(*args, **kwargs)