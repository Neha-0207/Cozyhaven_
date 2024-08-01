

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    distance = models.CharField(max_length=100)
    photos = models.JSONField(default=list)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    rooms = models.JSONField(default=list)
    cheapestPrice = models.FloatField()
    featured = models.BooleanField(default=False)
    


class Room(models.Model):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    KING = 'King'
    ROOM_TYPES = [
        (SINGLE, 'Single'),
        (DOUBLE, 'Double'),
        (KING, 'King'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    number_of_rooms = models.PositiveIntegerField(default=0)
    baseFare = models.FloatField()
    max_people = models.IntegerField()
   

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_fare = models.FloatField(default = 0.0)
    numOfGuest = models.IntegerField()

    def __str__(self):
        return f"Booking for {self.user.username} - Room: {self.room.title}"
