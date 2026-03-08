from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from datetime import date

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create your views here.


# movie_list takes request and renders movie_list.html with movie information
def movie_list(request):
    movie_info = Movie.objects.all()
    return render(request, "bookings/movie_list.html", {"Movie" : movie_info})

# seat_booking takes request and movie_id, renders seat_booking.html with seat information for specific movie_id
# Handles seat booking for user
def seat_booking(request, movie_id):
    movie_info = get_object_or_404(Movie, id = movie_id)
    seat_info = Seat.objects.all()

    if request.method == "POST":
        seat_number = request.POST.get("seat_number")
        username = request.POST.get("user")

        seat = get_object_or_404(Seat, seat_number = seat_number)

        if seat.booking_status == False:
            Booking.objects.create(movie = movie_info.title, seat = seat.seat_number, user = username, booking_date = date.today())
            
            seat.booking_status = True
            seat.save()

            return redirect("booking_history")

    return render(request, "bookings/seat_booking.html", {"Movie" : movie_info, "Seat" : seat_info})

# booking_history takes request and renders booking_history.html with booking history information
def booking_history(request):
    booking_info = Booking.objects.all()
    return render(request, "bookings/booking_history.html", {"Booking" : booking_info})

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

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