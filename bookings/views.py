from bookings.models import RentRequest, Favourite, Order
from bookings.serializers import RentRequestSerializer, UserRequestSerializer, UserAddRequestSerializer, UpdateRentRequestSerializer, FavouriteSerializer, OrderSerializer, OrderUpdateSerializer, EmptySerializer
from rest_framework import viewsets, exceptions, response, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.permissions import IsAdvertisementOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action


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

    @swagger_auto_schema(
        operation_summary='Get a list of rent request for an advertisement',
        operation_description='Only advertisement owner can get or see all the available rent requests for an their advertisements'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific rent request for an advertisement',
        operation_description='Only owner can see any specific rent request for their advertisement'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Only advertisement owner can accept/reject rent request',
        operation_description='Only advertisement owner can accept only one rent request from all the available requests. And when one request is accepted then he can not able to accept or reject any other request. Automatically other requests will be rejected for any specific advertisement'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class MyRentRequestViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserAddRequestSerializer
        return UserRequestSerializer
        
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return RentRequest.objects.none
        return RentRequest.objects.select_related('advertisement').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary='Get a list of rent request A user sent for advertisements',
        operation_description='Only User can get or see all the rent requests that they sent for advertisements'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Authenticated user can sent rent request for any advertisements',
        operation_description='Any authenticated user can sent rent requests for any advertisement that is not rented yet'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific rent request for an advertisement',
        operation_description='Only user can see any specific rent request they sent for an advertisement'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Authenticated user can delete their rent request',
        operation_description='Any authenticated user can delete rent requests they sent'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class FavouriteViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['GET', 'POST', 'DELETE']:
            return FavouriteSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Favourite.objects.none
        return Favourite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary='Get a list of advertisements user saved',
        operation_description='Only User can get or see all their rent advertisements they saved as favourite'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Authenticated user can save any advertisements links',
        operation_description='Any authenticated user can save advertisement links as their favourite by giving the advertisement id'
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve a specific rent advertisement saved as favourite',
        operation_description='Only user can see any specific rent advertisement links they saved as favourite'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Authenticated user can delete links they saved',
        operation_description='Any authenticated user can delete rent advertisement they saved as their favourite'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('advertisement').all()
        return Order.objects.select_related('advertisement').filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()

        if order.user != request.user:
            raise exceptions.PermissionDenied({'detail': 'You can only cancel your own order.'})
        if order.status == Order.BOOKED:
            raise exceptions.PermissionDenied({'detail': "You can not cancel this order. You already booked this."})
        
        order.status = Order.CANCELLED
        order.save()

        return response.Response(status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
        
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return OrderUpdateSerializer
        if self.action == 'cancel_order':
            return EmptySerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)