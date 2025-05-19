from advertisement.models import Category, Advertisement, AdvertisementImage, Review
from users.models import User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'advertise_count']

    advertise_count = serializers.IntegerField(read_only=True, help_text='Return the number of house advertisement in each category')

class AdvertisementImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image']


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_full_name')
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'profile_image', 'email', 'address', 'phone_number']

    def get_current_user_full_name(self, obj):
        return obj.get_full_name()
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None


class UpdateAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['status']

class AdvertisementSerializer(serializers.ModelSerializer):
    images = AdvertisementImageSerializer(many=True, read_only=True)
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'is_rented', 'category', 'status', 'owner', 'rental_amount', 'location', 'bedroom', 'bathroom', 'apartment_size', 'images', 'created_at']
        read_only_fields = ['status','is_rented', 'owner', 'created_at']
    
    def get_owner(self, obj):
        return SimpleUserSerializer(obj.owner).data

    def create(self, validated_data):
        user = self.context['user']
        return Advertisement.objects.create(owner=user, **validated_data)

    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = ['id', 'user', 'advertisement', 'rating', 'comment']
        read_only_fields = ['user', 'advertisement']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data