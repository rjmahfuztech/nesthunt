from users.serializers import MyAdvertisementSerializer
from rest_framework import viewsets, permissions, status, exceptions
from advertisement.models import Advertisement
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from users.models import User
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from djoser.views import UserViewSet
from django.contrib.auth.hashers import check_password
from advertisement.serializers import AdvertisementSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import requests


class MyAdvertisementViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete', 'put', 'options']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyAdvertisementSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Advertisement.objects.none
        return Advertisement.objects.prefetch_related('images').filter(owner=self.request.user)
    
    @swagger_auto_schema(
        operation_summary='Get a list of advertisement posted by owner',
        operation_description='Only advertisement owner can get or see all the advertisements they posted'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Owner can retrieve their any specific advertisement',
        operation_description='Only advertisement owner can retrieve their any specific advertisement'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Update a specific advertisement by owner',
        operation_description='Only advertisement Owner can update their advertisement'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific advertisement by Owner',
        operation_description='Only advertisement owner can delete their any specific advertisement'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class AdminDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Only admin view the dashboard',
        operation_description='Only admin can view all the statistics for this NestHunt project'
    )
    def list(self, request):
        today = now().date()
        first_day_current_month = today.replace(day=1)
        first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)

        statistic = Advertisement.objects.aggregate(
            total_advertisement=Count('id'),
            total_pending_advertisement=Count('id', filter=Q(status='Pending')),
            current_month_advertisement=Count('id', filter=Q(created_at__gte=first_day_current_month)),
            last_month_advertisement=Count('id', filter=Q(created_at__gte=first_day_last_month, created_at__lt=first_day_current_month))
        )

        advertisement = Advertisement.objects.select_related('owner').prefetch_related('images').all();

        return Response({**statistic, 'total_users': User.objects.count(), 'advertisements': AdvertisementSerializer(advertisement, many=True).data})
    

# Custom User viewSet
class CustomUserViewSet(UserViewSet):
    def destroy(self, request, *args, **kwargs):
        target_user = self.get_object()

        # admin can delete any user without password
        if request.user.is_staff or request.user.is_superuser:
            target_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # user can delete their own account with current password
        if request.user == target_user:
            current_password = request.data.get('current_password')
            if not current_password:
                raise exceptions.ValidationError({'current_password': 'This field is required.'})
            if not check_password(current_password, request.user.password):
                raise exceptions.ValidationError({'current_password': 'Password is incorrect.'})
            
            # delete user
            request.user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        # user can't delete other users
        raise exceptions.PermissionDenied('You do not have permission to delete this user.')
    
# Google Login
class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('access_token')
        if token is None:
            return Response({'error': 'No access token provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        google_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}"
        user_info = requests.get(google_url).json()

        if 'email' not in user_info:
            return Response({'error': 'Invalid access token.'}, status=status.HTTP_400_BAD_REQUEST)
        email = user_info['email']
        first_name = user_info['given_name']
        last_name = user_info['family_name']
        user, created = User.objects.get_or_create(email=email, defaults={'first_name': first_name, 'last_name': last_name})

        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
