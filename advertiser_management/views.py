from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404

from .models import Advertiser, Ad, View, Click
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.list import ListView

from django.db.models import Count, DateTimeField, When, Case, IntegerField, OuterRef, Subquery, Q, F, ExpressionWrapper, DurationField, Avg
from django.db.models.functions import TruncHour

# Create your views here.

    
class AdCreateView(TemplateView):
    template_name = "advertiser_management/create_ad.html"

    def post(self, request, *args, **kwargs):
        advertiser_id = request.POST["advertiser_id"]
        try:
            advertiser = Advertiser.objects.get(pk=advertiser_id)

        except Advertiser.DoesNotExist:
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
            if ad.approved:
                ad.view_set.create(user_ip=request.user_ip)


        return super().get(self, request, *args, **kwargs)
    
class AdRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs["ad_id"])
        ad.click_set.create(user_ip=self.request.user_ip)
        self.url = ad.link
        return super().get_redirect_url(*args, **kwargs)
    
class AdReportView(TemplateView):
    template_name = "advertiser_management/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ad_id = kwargs["ad_id"]
        ad = get_object_or_404(Ad, pk=ad_id)
        if(ad.approved == False):
            raise Http404
        
        #first report
        views_by_every_hour = ad.view_set.values("datetime__hour").annotate(total_views=Count("datetime__hour"))
        views_by_every_hour_list = [0] * 24
        for view in views_by_every_hour:
            views_by_every_hour_list[view["datetime__hour"]] = view["total_views"]

        context["views_every_hour"] = views_by_every_hour_list

        clicks_by_every_hour = ad.click_set.values("datetime__hour").annotate(total_clicks=Count("datetime__hour"))
        clicks_by_every_hour_list = [0] * 24
        for click in clicks_by_every_hour:
            clicks_by_every_hour_list[click["datetime__hour"]] = click["total_clicks"]

        context["clicks_every_hour"] = clicks_by_every_hour_list


        #socond report
        click_view_rate = ad.click_set.count() / ad.view_set.count()
        
        context["click_view_rate"] = click_view_rate



        #third report
        avg_difference_click_view = (ad.click_set.annotate(
            latest_view=Subquery(
                View.objects.filter(ad=ad_id, datetime__lt=OuterRef("datetime"), user_ip=OuterRef("user_ip"))
                .order_by("-datetime")
                .values("datetime")[:1]
            )
        )
        .annotate(difference=ExpressionWrapper(F('datetime') - F('latest_view'), output_field=DurationField()))
        .aggregate(Avg("difference")))
    
        context["avg_difference_click_view"] = avg_difference_click_view["difference__avg"].seconds

        


        return context
