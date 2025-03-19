from rest_framework import serializers
from advertisement.models import Advertisement


class MyAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'category', 'status', 'location', 'bedroom', 'bathroom', 'rental_amount', 'apartment_size']
        read_only_fields = ['status', 'category']