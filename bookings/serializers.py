from bookings.models import RentRequest, Favourite
from advertisement.models import Advertisement
from rest_framework import serializers
from advertisement.serializers import SimpleUserSerializer

class SimpleAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'location', 'bedroom', 'bathroom', 'rental_amount']

class RentRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = RentRequest
        fields = ['id', 'advertisement', 'user', 'status']
        read_only_fields = ['user', 'status']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

class UpdateRentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentRequest
        fields = ['status']


class UserRequestSerializer(serializers.ModelSerializer):
    advertisement = SimpleAdvertisementSerializer(read_only=True)
    class Meta:
        model = RentRequest
        fields = ['id', 'advertisement', 'status']
        read_only_fields = ['status']


class UserAddRequestSerializer(serializers.ModelSerializer):
    advertisement_id = serializers.IntegerField()
    class Meta:
        model = RentRequest
        fields = ['id', 'status', 'advertisement_id']
        read_only_fields = ['status']

    def validate_advertisement_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('Your advertisement Id must be 1 or bigger value')
        elif not Advertisement.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'Advertisement with id {value} does not exist')
        elif not Advertisement.objects.filter(pk=value, status='Approved'):
            raise serializers.ValidationError(f'Advertisement with Id {value} is not verified by Admin')
        elif RentRequest.objects.filter(advertisement_id=value, user=self.context['request'].user).exists():
            raise serializers.ValidationError('You have already requested for this advertisement')
        elif Advertisement.objects.filter(pk=value , is_rented=True).exists():
            raise serializers.ValidationError("You can't send Rent request. This advertisement is already booked for rent")
        elif Advertisement.objects.filter(pk=value, owner=self.context['request'].user).exists():
            raise serializers.ValidationError("This is your advertisement! you can't send rent request")
        
        return value

    def create(self, validated_data):
        advertisement_id = validated_data['advertisement_id']
        user = validated_data['user']

        return RentRequest.objects.create(user=user, advertisement_id=advertisement_id)


class FavouriteSerializer(serializers.ModelSerializer):
    advertisement_id = serializers.IntegerField(write_only=True)
    advertisement = serializers.HyperlinkedRelatedField(
        view_name = 'advertisements-detail',
        read_only=True
    )

    class Meta:
        model = Favourite
        fields = ['id', 'advertisement_id', 'advertisement']

    def validate_advertisement_id(self, value):
        if value < 0:
            raise serializers.ValidationError('Your advertisement Id must be a positive value')
        elif not Advertisement.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'Advertisement with id {value} does not exist')
        elif not Advertisement.objects.filter(pk=value, status='Approved'):
            raise serializers.ValidationError(f'Advertisement with Id {value} is not verified by Admin')
        elif Favourite.objects.filter(advertisement_id=value, user=self.context['request'].user).exists():
            raise serializers.ValidationError('You have already saved this advertisement in your Favourite list!')
        
        return value

    def create(self, validated_data):
        advertisement_id = validated_data['advertisement_id']
        user = validated_data['user']

        return Favourite.objects.create(user=user, advertisement_id=advertisement_id)