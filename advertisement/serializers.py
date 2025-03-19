from advertisement.models import Category, Advertisement, AdvertisementImage, Review
from users.models import User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image']

class EmptySerializer(serializers.Serializer):
    pass

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

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_full_name')
    class Meta:
        model = User
        fields = ['id', 'name']

    def get_current_user_full_name(self, obj):
        return obj.get_full_name()
    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = ['id', 'user', 'advertisement', 'rating', 'comment']
        read_only_fields = ['user', 'advertisement']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data