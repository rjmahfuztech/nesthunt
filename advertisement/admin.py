from django.contrib import admin
from advertisement.models import Category, Advertisement, AdvertisementImage, Review

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(AdvertisementImage)
admin.site.register(Review)
