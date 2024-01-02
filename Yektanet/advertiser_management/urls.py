from django.urls import path
from . import views


app_name = "advertiser_management"

urlpatterns = [
    path("create_ad/", views.new_ad, name="create_ad"),
    path("ads/", views.ads, name="ads"),
    path("redirect/<int:ad_id>/", views.RedirectToAdLink.as_view(), name="redirect")
]