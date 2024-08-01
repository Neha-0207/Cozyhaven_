from django.urls import path
from .views import UserRegistration, UserLogin
from .views import *;
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views



urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_register'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('hotels/', HotelListAPIView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel-detail'),
    # path('rooms/', RoomListCreateAPIView.as_view(), name='room-list'),
    # path('rooms/<int:pk>/', RoomRetrieveUpdateDestroyAPIView.as_view(), name='room-detail'),
    path('rooms/<int:room_id>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('hotels/<int:hotel_id>/rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('hotels/<int:hotel_id>/rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('bookings/', views.booking_list, name='booking-list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking-detail'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]