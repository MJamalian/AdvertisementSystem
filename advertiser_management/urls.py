from django.urls import path
from . import views


app_name = "advertiser_management"

urlpatterns = [
    path("create_ad/", views.AdCreateView.as_view(), name="create_ad"),
    path("ads/", views.AdShowView.as_view(), name="show_ads"),
    path("redirect/<int:ad_id>/", views.AdRedirectView.as_view(), name="redirect"),
    path("report/ad/<int:ad_id>", views.AdReportView.as_view(), name="report")
]