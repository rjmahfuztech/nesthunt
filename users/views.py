from django.shortcuts import render
from users.serializers import MyAdvertisementSerializer
from rest_framework import viewsets, permissions
from advertisement.models import Advertisement

class MyAdvertisementViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete', 'put', 'options']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyAdvertisementSerializer

    def get_queryset(self):
        return Advertisement.objects.filter(owner=self.request.user)

