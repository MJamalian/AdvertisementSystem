from django.urls import path
from . import views


app_name = "advertiser_management"

urlpatterns = [
    path('new_ad/', views.new_ad, name='new_ad'),
    path('ads/', views.ads, name="ads")
]