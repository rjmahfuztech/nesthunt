from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from api.permissions import IsAdminOrReadOnly
from advertisement.models import Advertisement, Category, AdvertisementImage
from advertisement import serializers
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class AdvertisementViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'location', 'bedroom', 'bathroom']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Advertisement.objects.all()
        return Advertisement.objects.filter(status='Approved')
    
    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.UpdateAdvertisementSerializer
        return serializers.AdvertisementSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}
    

class AdvertisementImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.AdvertisementImageSerializer

    def get_queryset(self):
        return AdvertisementImage.objects.filter(advertisement_id=self.kwargs.get('advertisement_pk'))
    
    def perform_create(self, serializer):
        serializer.save(advertisement_id=self.kwargs.get('advertisement_pk'))

