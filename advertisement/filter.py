from django_filters.rest_framework import FilterSet
from advertisement.models import Advertisement

class AdvertiseFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields = {
            'category_id': ['exact'],
            'rental_amount' : ['gt', 'lt'],
            'bedroom': ['exact'],
            'bathroom': ['exact']
        }