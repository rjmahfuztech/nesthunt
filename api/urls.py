from django.urls import path, include
from rest_framework_nested import routers
from advertisement.views import AdvertisementViewSet, CategoryViewSet, AdvertisementImageViewSet, ReviewViewSet
from bookings.views import MyRentViewSet, MyRentRequestViewSet, FavouriteViewSet

router = routers.DefaultRouter()

router.register('advertisements', AdvertisementViewSet, basename='advertisements')
router.register('categories', CategoryViewSet, basename='categories')
router.register('my_rents', MyRentViewSet, basename='my-rents')
router.register('my_rent_requests', MyRentRequestViewSet, basename='my-rent-requests')
router.register('favourites', FavouriteViewSet, basename='favourites')

advertisement_router = routers.NestedDefaultRouter(router, 'advertisements', lookup='advertisement')
advertisement_router.register('images', AdvertisementImageViewSet, basename='advertisement-image')
advertisement_router.register('reviews', ReviewViewSet, basename='advertisement-review')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(advertisement_router.urls))
]
