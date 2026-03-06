from django.shortcuts import render, HttpResponse
from .models import Movie, Seat, Booking

# Create your views here.


def Base(request):
    return render(request, "base.html")

def MovieViewSet(request):
    movie_info = Movie.objects.all()
    return render(request, "movie_list.html", {"Movie" : movie_info})

def SeatViewSet(request):
    seat_info = Seat.objects.all()
    return render(request, "seat_booking.html", {"Seat" : seat_info})

def BookingViewSet(request):
    booking_info = Booking.objects.all()
    return render(request, "booking_history.html", {"Booking" : booking_info})