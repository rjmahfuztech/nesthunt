from django.shortcuts import render
from bookings.models import RentRequest, Favourite
from bookings.serializers import RentRequestSerializer, UserRequestSerializer, UpdateRentRequestSerializer, FavouriteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdvertisementOwnerOrReadOnly


class RentRequestViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'head', 'options']
    permission_classes = [IsAdvertisementOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RentRequestSerializer
        return UpdateRentRequestSerializer
        
    def get_queryset(self):
        return RentRequest.objects.filter(advertisement_id=self.kwargs.get('my_advertisement_pk'))


class MyRentRequestViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]
    serializer_class = UserRequestSerializer
        
    def get_queryset(self):
        return RentRequest.objects.select_related('advertisement').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['GET', 'POST', 'DELETE']:
            return FavouriteSerializer

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)