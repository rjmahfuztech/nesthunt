from django.shortcuts import render
from bookings.models import RentRequest, Favourite
from bookings.serializers import RentRequestSerializer, UpdateRentRequestSerializer, FavouriteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# class RentRequestViewSet(viewsets.ModelViewSet):
#     serializer_class = RentRequestSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """
#         Default queryset (fallback) - If no action is specified, return empty queryset.
#         """
#         return RentRequest.objects.none()  

#     @action(detail=False, methods=['get', 'delete'])
#     def my_requests(self, request):
#         """
#         Users can see the rent requests they sent.
#         """
#         queryset = RentRequest.objects.filter(user=request.user)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get', 'patch'])
#     def my_rents(self, request):
#         """
#         Owners can see rent requests for their advertisements.
#         """
#         queryset = RentRequest.objects.filter(advertisement__owner=request.user)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class MyRentRequestViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['GET', 'POST', 'DELETE']:
            return RentRequestSerializer
        
    def get_queryset(self):
        return RentRequest.objects.select_related('user').select_related('advertisement').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyRentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RentRequestSerializer
        return UpdateRentRequestSerializer
        
    def get_queryset(self):
        return RentRequest.objects.select_related('user').select_related('advertisement').filter(advertisement__owner=self.request.user)
    
    def perform_update(self, serializer):
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