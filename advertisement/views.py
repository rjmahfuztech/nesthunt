from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from api.permissions import IsAdminOrReadOnly, IsAdvertisementOwnerOrReadOnly
from advertisement.models import Advertisement, Category, AdvertisementImage, Review
from advertisement import serializers
from django_filters.rest_framework import DjangoFilterBackend
from advertisement.permissions import IsReviewAuthorOrReadOnly
from rest_framework.exceptions import PermissionDenied


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class AdvertisementViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'options']
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'location', 'bedroom', 'bathroom']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Advertisement.objects.prefetch_related('images').all()
        return Advertisement.objects.prefetch_related('images').filter(status='Approved')
    
    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return serializers.UpdateAdvertisementSerializer
        return serializers.AdvertisementSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}
    

class AdvertisementImageViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'options']

    permission_classes = [IsAdvertisementOwnerOrReadOnly]
    serializer_class = serializers.AdvertisementImageSerializer

    def get_queryset(self):
        return AdvertisementImage.objects.filter(advertisement_id=self.kwargs.get('my_advertisement_pk'))
    
    def perform_create(self, serializer):
        advertisement = Advertisement.objects.get(pk=self.kwargs.get('my_advertisement_pk'))

        if advertisement.owner != self.request.user:
            raise PermissionDenied('You do not have permission to add image for the Advertisement!')
        serializer.save(advertisement=advertisement)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.select_related('user').filter(advertisement_id=self.kwargs.get('advertisement_pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, advertisement_id=self.kwargs.get('advertisement_pk'))


