from django.shortcuts import render
from bookings.models import RentRequest, Favourite
from bookings.serializers import RentRequestSerializer, UserRequestSerializer, UpdateRentRequestSerializer, FavouriteSerializer
from rest_framework import viewsets, exceptions
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
    
    def perform_update(self, serializer):
        # checking any request is approved or not
        rent_request = self.get_object()
        if rent_request.advertisement.is_rented == True:
            raise exceptions.PermissionDenied("You have already accepted a request. You can't update any request for this advertisement.")
        
        # update
        rent_request = serializer.save()

        if rent_request.status == RentRequest.APPROVED:
            advertisement = rent_request.advertisement

            advertisement.is_rented = True
            advertisement.save()

            RentRequest.objects.filter(advertisement=advertisement, status=RentRequest.PENDING).exclude(id=rent_request.id).update(status=RentRequest.REJECTED)


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