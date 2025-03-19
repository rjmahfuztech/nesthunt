from django.shortcuts import render
from bookings.models import RentRequest, Favourite
from bookings.serializers import RentRequestSerializer, FavouriteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class RentRequestViewSet(viewsets.ModelViewSet):
    # queryset = RentRequest.objects.all()
    serializer_class = RentRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RentRequest.objects.filter(user=self.request.user)
        

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