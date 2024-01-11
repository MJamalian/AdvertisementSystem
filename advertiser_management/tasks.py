from Yektanet.celery import app

from .models import View, Click, HourlyClicks, HourlyViews, Ad

from datetime import timedelta
from django.utils import timezone

from django.db.models import Count, Sum



@app.task
def count_views_clicks_every_hour():
    last_hour_views = (View.objects
        .filter(datetime__range=(timezone.now() - timedelta(hours=1), timezone.now()))
        .values("ad")
        .annotate(views_count=Count("ad"))
    )

    HourlyViews.objects.bulk_create(map(lambda el: HourlyViews(ad=Ad.objects.get(pk=el["ad"]), views_count=el["views_count"]), last_hour_views))

    last_hour_clicks = (Click.objects
        .filter(datetime__range=(timezone.now() - timedelta(hours=1), timezone.now()))
        .values("ad")
        .annotate(clicks_count=Count("ad"))
    )

    HourlyClicks.objects.bulk_create(map(lambda el: HourlyClicks(ad=Ad.objects.get(pk=el["ad"]), clicks_count=el["clicks_count"]), last_hour_clicks))



@app.task
def count_views_clicks_every_day():
    last_day_views = (HourlyViews.objects
        .values("ad")
        .annotate(total_views=Sum("views_count"))                  
    )
    print(last_day_views)
    HourlyViews.objects.all().delete()

    last_day_clicks = (HourlyClicks.objects
        .values("ad")
        .annotate(total_clicks=Sum("clicks_count"))                  
    )
    print(last_day_clicks)
    HourlyClicks.objects.all().delete()