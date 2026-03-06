from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    release_date = models.CharField(max_length = 255)
    duration = models.CharField(max_length = 255)

class Seat(models.Model):
    seat_number = models.CharField(max_length = 255)
    booking_status = models.BooleanField(default = False)

class Booking(models.Model):
    movie = models.CharField(max_length = 255)
    seat = models.CharField(max_length = 255)
    user = models.CharField(max_length = 255)
    booking_date = models.CharField(max_length = 255)