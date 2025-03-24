from users.serializers import MyAdvertisementSerializer
from rest_framework import viewsets, permissions
from advertisement.models import Advertisement
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from users.models import User
from django.db.models import Count, Q

class MyAdvertisementViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete', 'put', 'options']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyAdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(owner=self.request.user)
    

class AdminDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    
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

        return Response({**statistic, 'total_users': User.objects.count()})