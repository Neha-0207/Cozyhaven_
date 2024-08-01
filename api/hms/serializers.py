from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','check_in_date', 'check_out_date', 'numOfGuest', 'room', 'total_fare']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'user' field from required fields
        required_fields = set(self.fields.keys())
        if 'user' in required_fields:
            required_fields.remove('user')
        self.required_fields = required_fields

    def get_hotel_name(self, obj):
        return obj.room.hotel.name