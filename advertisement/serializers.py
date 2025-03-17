from advertisement.models import Category, Advertisement, AdvertisementImage
from users.models import User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image']

class UpdateAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['status']

class AdvertisementSerializer(serializers.ModelSerializer):
    images = AdvertisementImageSerializer(many=True, read_only=True)
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'category', 'status', 'owner', 'rental_amount', 'location', 'bedroom', 'bathroom', 'apartment_size', 'images']
        read_only_fields = ['status', 'owner']

    def create(self, validated_data):
        user = self.context['user']
        return Advertisement.objects.create(owner=user, **validated_data)