from django.urls import path, include
from . import views
from rest_framework import routers



app_name = "advertiser_management"

router = routers.DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'report/ads', views.ReportViewSet, basename="report-detail")

urlpatterns = [
    path("", include(router.urls))
]