from bookings.models import RentRequest, Favourite
from advertisement.models import Advertisement
from rest_framework import serializers


class RentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentRequest
        fields = ['id', 'advertisement', 'user', 'status']
        read_only_fields = ['user', 'status']


class FavouriteSerializer(serializers.ModelSerializer):
    advertisement = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.filter(status='Approved'),
        write_only=True
    )
    advertisement_url = serializers.HyperlinkedIdentityField(
        view_name = 'advertisements-detail',
        read_only=True
    )
    class Meta:
        model = Favourite
        fields = ['id', 'advertisement', 'advertisement_url']