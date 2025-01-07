from tkinter.font import names

from rest_framework import routers
from .views import *
from django.urls import path, include



router = routers.DefaultRouter()
router.register(r'booking', BookingViewSet, basename='booking_list'),
router.register(r'rating', RatingViewSet, basename='rating_list')


urlpatterns = [
    path('', include(router.urls)),
    path('room/', RoomListAPIView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailAPIView.as_view(), name='room_detail'),
    path('hotel/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('country/', CountryListAPIView.as_view(), name='country_list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country_detail'),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('review/', ReviewListAPIView.as_view(), name='review_list'),
    path('review/<int:pk>/', ReviewDetailAPIView.as_view(), name='review_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]