from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from api.permissions import IsAdminOrReadOnly, IsAdvertisementOwnerOrReadOnly
from advertisement.models import Advertisement, Category, AdvertisementImage, Review
from advertisement import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from advertisement.permissions import IsReviewAuthorOrReadOnly
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from advertisement.filter import AdvertiseFilter
from django.db.models import Count


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'put', 'options']

    queryset = Category.objects.annotate(advertise_count=Count('advertisements')).all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Get a list of category',
        operation_description='Any user can get or see all the available categories'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a category by Admin',
        operation_description='Only Admin can create or add a category'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific category',
        operation_description='Any user can retrieve any specific category'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a specific category by Admin',
        operation_description='Only Admin can update any specific category'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific category by Admin',
        operation_description='Only Admin can Delete any specific category'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AdvertisementViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'options']
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AdvertiseFilter
    search_fields = ['title', 'location']

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
    
    @swagger_auto_schema(
        operation_summary='Get a list of advertisement',
        operation_description='Any user can get or see all the available advertisements'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a advertisement by authenticated user',
        operation_description='Any authenticated user can create or add an advertisement'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific advertisement',
        operation_description='Any user can retrieve any specific advertisement'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a specific advertisement status by Admin',
        operation_description='Only Admin can approve or reject any specific advertisement posted by authenticated user'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific advertisement by Admin',
        operation_description='Only Admin can Delete any specific advertisement'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

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

    @swagger_auto_schema(
        operation_summary='Get a list of images for an advertisement',
        operation_description='Any user can get or see all the available images for an advertisements'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Set images for an advertisement by owner',
        operation_description='Only advertisement owner can set or add images for their advertisement'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific images for an advertisement',
        operation_description='Any user can see any specific images for an advertisement'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific image for an advertisement by owner',
        operation_description='Only advertisement owner/admin can Delete any specific images for an advertisement'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'options']

    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.select_related('user').filter(advertisement_id=self.kwargs.get('advertisement_pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, advertisement_id=self.kwargs.get('advertisement_pk'))

    @swagger_auto_schema(
        operation_summary='Get a list of reviews for an advertisement',
        operation_description='Any user can get or see all the available reviews for an advertisements'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a review for an advertisement',
        operation_description='Any authenticated user can create or add a review an advertisement'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific review for an advertisement',
        operation_description='Any user can retrieve any specific review for an advertisement'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a specific review for an advertisement by owner',
        operation_description='Only Review Owner/admin can update their review for an advertisement'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific review for an advertisement by Admin',
        operation_description='Only Admin can Delete any specific review for an advertisement'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


