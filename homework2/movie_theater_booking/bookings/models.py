from django.db import models

# Create your models here.


# Movie model, consists of title, description, release_date, and duration
class Movie(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField()

# Seat model, consists of seat_number and booking_status
class Seat(models.Model):
    seat_number = models.CharField(max_length = 15)
    booking_status = models.BooleanField(default = False)

# Booking model, consists of movie, seat, user, and booking_date
class Booking(models.Model):
    movie = models.CharField(max_length = 255)
    seat = models.CharField(max_length = 15)
    user = models.CharField(max_length = 255)
    booking_date = models.DateField()