from rest_framework import serializers
from advertisement.models import Advertisement
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class MyAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'category', 'status', 'location', 'bedroom', 'bathroom', 'rental_amount', 'apartment_size']
        read_only_fields = ['status', 'category']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number', 'profile_image']