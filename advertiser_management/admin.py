from django.contrib import admin
from .models import Ad

# Register your models here.

class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "advertiser", "approved")
    search_fields = ["title"]
    list_filter = ("approved",)

admin.site.register(Ad, AdAdmin)

