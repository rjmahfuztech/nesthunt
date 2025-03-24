from django.urls import path, include
from rest_framework_nested import routers
from advertisement.views import AdvertisementViewSet, CategoryViewSet, AdvertisementImageViewSet, ReviewViewSet
from bookings.views import RentRequestViewSet, MyRentRequestViewSet, FavouriteViewSet
from users.views import MyAdvertisementViewSet, AdminDashboardViewSet

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('advertisements', AdvertisementViewSet, basename='advertisements')
router.register('my_advertisements', MyAdvertisementViewSet, basename='my-advertisements')
router.register('my_rent_requests', MyRentRequestViewSet, basename='my_rent-requests')
router.register('favourites', FavouriteViewSet, basename='favourites')
router.register('admin/dashboard', AdminDashboardViewSet, basename='dashboard')

advertisement_router = routers.NestedDefaultRouter(router, 'advertisements', lookup='advertisement')
advertisement_router.register('reviews', ReviewViewSet, basename='advertisement-reviews')

my_advertisement_router = routers.NestedDefaultRouter(router, 'my_advertisements', lookup='my_advertisement')
my_advertisement_router.register('images', AdvertisementImageViewSet, basename='advertisement-images')
my_advertisement_router.register('rent_requests', RentRequestViewSet, basename='rent-requests')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(advertisement_router.urls)),
    path('', include(my_advertisement_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
