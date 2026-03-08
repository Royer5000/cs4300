from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

from .models import Movie, Seat, Booking

# Create your tests here.

class ModelTests(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title = "Spider Man: Into the Spider-Verse",
            description = "Spider Man, but animated, with Miles Morales",
            release_date = date.today(),
            duration = 116
        )

        self.seat = Seat.objects.create(
            seat_number = 3,
            booking_status = False
        )
    
    def test_movie_list(self):
        self.assertEqual(self.movie.title, "Spider Man: Into the Spider-Verse")

    def test_default_seat_status(self):
        self.assertFalse(self.seat.booking_status)

    def test_seat_booking(self):
        booking = Booking.objects.create(
            movie = "Spider Man: Into the Spider-Verse",
            seat = 3,
            user = "Jayden",
            booking_date = date.today()
        )

        self.assertEqual(booking.user, "Jayden")
        self.assertEqual(booking.seat, 3)


class APITests(APITestCase):
    
    def setUp(self):
        self.movie = Movie.objects.create(
            title = "Mean Girls",
            description = "PG-13 Comedy, it's Mean Girls",
            release_date = date.today(),
            duration = 98
        )

        self.seat = Seat.objects.create(
            seat_number = 15,
            booking_status = False
        )

        self.seat = Seat.objects.create(
            seat_number = 7,
            booking_status = True
        )

    def test_movies_list(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_create_movie(self):
        data = {
            "title" : "The Breakfast Club",
            "description" : "High school detention students make a group",
            "release_date" : str(date.today()),
            "duration" : 97
        }
        response = self.client.post("/api/movies/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_seat_booking(self):
        response = self.client.get("/api/seats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking_successful_booking(self):
        data = {
            "movie" : "The Breakfast Club",
            "seat" : 15,
            "user" : "Jayden890!"
        }

        response = self.client.post("/api/bookings/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.seat.refresh_from_db()
        self.assertTrue(self.seat.booking_status)
    
    def test_create_booking_invalid_seat_number(self):
        data = {
            "movie" : "The Breakfast Club",
            "seat" : 666,
            "user" : "Jayden890!"
        }

        response = self.client.post("/api/bookings/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_booking_already_booked(self):
        self.seat.booking_status = True
        self.seat.save()

        data = {
            "movie": "The Breakfast Club",
            "seat": 7,
            "user": "Jayden890!"
        }

        response = self.client.post("/api/bookings/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_booking_history(self):
        Booking.objects.create(
            movie = "The Breakfast Club",
            seat = 15,
            user = "Jayden890!",
            booking_date = date.today()
        )

        response = self.client.get("/api/bookings/history/?user=Jayden890!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_booking_history_without_user(self):
        response = self.client.get("/api/bookings/history/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)