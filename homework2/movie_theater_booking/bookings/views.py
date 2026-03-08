from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from datetime import date
import requests

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create your views here.


# movie_list takes request and renders movie_list.html with movie information
def movie_list(request):
    url = "https://mysite-b2np.onrender.com/api/movies/"
    response = requests.get(url)
    movies = response.json()
    return render(request, "bookings/movie_list.html", {"movies" : movies})

# seat_booking takes request and movie_id, renders seat_booking.html with seat information for specific movie_id
# Handles seat booking for user
def seat_booking(request, movie_id):
    movie_url = f"https://mysite-b2np.onrender.com/api/movies/{movie_id}/"
    movie_response = requests.get(movie_url)
    movie = movie_response.json()

    seats_url = "https://mysite-b2np.onrender.com/api/seats/"
    seats_response = requests.get(seats_url)
    seats = seats_response.json()

    if request.method == "POST":
        seat_number = request.POST.get("seat_number")
        username = request.POST.get("user")

        selected_seat = next((s for s in seats if s["seat_number"] == seat_number), None)

        if not selected_seat:
            return render(request, "bookings/seat_booking.html", {
                "movie" : movie,
                "seats" : seats,
                "error" : "Seat does nnot exist."
            })

        if selected_seat["booking_status"] == True:
            return render(request, "bookings/seat_booking.html", {
                "movie" : movie,
                "seats" : seats,
                "error" : "Seat is already booked."
            })
        
        # Create booking through Render API
        booking_url = "https://mysite-b2np.onrender.com/api/bookings/"
        booking_payload = {
            "movie" : movie["title"],
            "seat" : seat_number,
            "user" : username
        }
        requests.post(booking_url, json=booking_payload)

        return redirect("booking_history")

    return render(request, "bookings/seat_booking.html", {
        "movie" : movie,
        "seats" : seats
    })

# booking_history takes request and renders booking_history.html with booking history information
def booking_history(request):
    url = "https://mysite-b2np.onrender.com/api/bookings/"
    response = requests.get(url)
    bookings = response.json()

    return render(request, "bookings/booking_history.html", {"bookings": bookings})


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kargs):
        movie_title = request.data.get("movie")
        seat_number = request.data.get("seat")
        username = request.data.get("user")

        try:
            seat = Seat.objects.get(seat_number = seat_number)
        except Seat.DoesNotExist:
            return Response({"error" : "Seat not found"}, status = status.HTTP_404_NOT_FOUND)
        
        if seat.booking_status:
            return Response({"error" : "Seat is already booked"}, status = status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(movie = movie_title, seat = seat_number, user = username, booking_date = date.today())
            
        seat.booking_status = True
        seat.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def history(self, request):
        username = request.query_params.get("user")

        if not username:
            return Response({"error": "Missing user"}, status = status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(user = username)
        serializer = BookingSerializer(bookings, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)