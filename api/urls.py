from django.urls import path, include
from rest_framework_nested import routers
from advertisement.views import AdvertisementViewSet, CategoryViewSet, AdvertisementImageViewSet, ReviewViewSet
from bookings.views import RentRequestViewSet, MyRentRequestViewSet, FavouriteViewSet, OrderViewSet, payment_initiate, payment_success, payment_fail, payment_cancel, HasHouseRented
from users.views import MyAdvertisementViewSet, AdminDashboardViewSet, CustomUserViewSet, GoogleLoginView

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('advertisements', AdvertisementViewSet, basename='advertisements')
router.register('my_advertisements', MyAdvertisementViewSet, basename='my-advertisements')
router.register('my_rent_requests', MyRentRequestViewSet, basename='my-rent-requests')
router.register('favourites', FavouriteViewSet, basename='favourites')
router.register('admin/dashboard', AdminDashboardViewSet, basename='dashboard')
router.register('auth/users', CustomUserViewSet, basename='user')
router.register('orders', OrderViewSet, basename='orders')

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
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('payment/initiate/', payment_initiate, name='payment-initiate'),
    path('payment/success/', payment_success, name='payment-success'),
    path('payment/fail/', payment_fail, name='payment-fail'),
    path('payment/cancel/', payment_cancel, name='payment-cancel'),
    path('orders/has_rented/<int:advertise_id>/', HasHouseRented.as_view(), name='has-rented')
]
