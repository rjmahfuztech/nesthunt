from django.urls import path, include
from rest_framework_nested import routers
from advertisement.views import AdvertisementViewSet, CategoryViewSet, AdvertisementImageViewSet, ReviewViewSet

router = routers.DefaultRouter()

router.register('advertisements', AdvertisementViewSet, basename='advertisements')
router.register('categories', CategoryViewSet, basename='categories')

advertisement_router = routers.NestedDefaultRouter(router, 'advertisements', lookup='advertisement')
advertisement_router.register('images', AdvertisementImageViewSet, basename='advertisement-image')
advertisement_router.register('reviews', ReviewViewSet, basename='advertisement-review')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(advertisement_router.urls))
]
