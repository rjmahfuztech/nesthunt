from rest_framework import serializers
from advertisement.models import Advertisement
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from advertisement.serializers import AdvertisementImageSerializer


class MyAdvertisementSerializer(serializers.ModelSerializer):
    images = AdvertisementImageSerializer(many=True, read_only=True)
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'category', 'status', 'location', 'bedroom', 'bathroom', 'rental_amount', 'apartment_size', 'images']
        read_only_fields = ['status', 'category']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']

class UserSerializer(BaseUserSerializer):
    profile_image = serializers.ImageField(required=False)
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'profile_image']