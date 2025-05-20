from django.contrib import admin
from bookings.models import RentRequest, Favourite, Order

admin.site.register(RentRequest)
admin.site.register(Favourite)
admin.site.register(Order)
