from .serializers import AdSerializer

from .models import Ad, View

from .permissions import IsOwnerOrReadOnly, IsOwner

from django.db.models import Count, OuterRef, Subquery, Q, F, ExpressionWrapper, DurationField, Avg, Sum

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions


# Create your views here.

class AdViewSet(viewsets.GenericViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.filter(approved=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        View.objects.bulk_create([(View(user_ip=request.user_ip, ad=ad)) for ad in self.get_queryset()])
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        ad = self.get_object()
        ad.clicks.create(user_ip=request.user_ip)
        serializer = self.get_serializer(ad)
        return Response(serializer.data)
    

class ReportViewSet(viewsets.GenericViewSet):
    queryset = Ad.objects.all()
    permission_classes = [IsOwner]

    def retrieve(self, request, pk):
        ad = self.get_object()
        result = {}

        views_by_every_hour = ad.views.values("datetime__hour").annotate(total_views=Count("datetime__hour"))
        views_by_every_hour_list = [0] * 24
        for view in views_by_every_hour:
            views_by_every_hour_list[view["datetime__hour"]] = view["total_views"]

        result["views_by_every_hour"] = views_by_every_hour_list

        clicks_by_every_hour = ad.clicks.values("datetime__hour").annotate(total_clicks=Count("datetime__hour"))
        clicks_by_every_hour_list = [0] * 24
        for click in clicks_by_every_hour:
            clicks_by_every_hour_list[click["datetime__hour"]] = click["total_clicks"]

        result["clicks_by_every_hour"] = clicks_by_every_hour_list

        if ad.views.count() == 0:
            click_view_rate = 0
        else:
            click_view_rate = ad.clicks.count() / ad.views.count()

        result["click_view_rate"] = click_view_rate

        avg_difference_click_view = (ad.clicks.annotate(
            latest_view=Subquery(
                View.objects.filter(ad=pk, datetime__lt=OuterRef("datetime"), user_ip=OuterRef("user_ip"))
                .order_by("-datetime")
                .values("datetime")[:1]
            )
        )
        .annotate(difference=ExpressionWrapper(F('datetime') - F('latest_view'), output_field=DurationField()))
        .aggregate(Avg("difference")))

        if avg_difference_click_view["difference__avg"] == None:
            result["Avg_difference_click_view"] = 0
        else:
            result["Avg_difference_click_view"] = avg_difference_click_view["difference__avg"].seconds

        return Response(result, status=status.HTTP_200_OK)