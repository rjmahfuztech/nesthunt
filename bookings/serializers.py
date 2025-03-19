from bookings.models import RentRequest, Favourite
from advertisement.models import Advertisement
from rest_framework import serializers


class RentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentRequest
        fields = ['id', 'advertisement', 'user', 'status']
        read_only_fields = ['user', 'status']


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
            raise serializers.ValidationError(f'Advertisement with Id {value} not verified by Admin')
        elif Favourite.objects.filter(advertisement_id=value, user=self.context['request'].user).exists():
            raise serializers.ValidationError('You have already saved this advertisement in your Favourite list!')
        
        return value

    def create(self, validated_data):
        advertisement_id = validated_data['advertisement_id']
        user = validated_data['user']

        return Favourite.objects.create(user=user, advertisement_id=advertisement_id)