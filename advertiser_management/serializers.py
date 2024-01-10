from rest_framework import serializers
from .models import Advertiser, Ad, Click, View

class AdvertiserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertiser
        fields = ["id", "name", "ads"]

class AdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ad
        fields = ["id", "title", "img_url", "link", "advertiser"]

