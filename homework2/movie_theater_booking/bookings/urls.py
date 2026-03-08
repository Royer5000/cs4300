from django.urls import path
from . import views


urlpatterns = [
    path("", views.movie_list, name = "Home"),
    path("movie/", views.movie_list, name = "movie_list"),
    path("book/<int:movie_id>/", views.seat_booking, name = "seat_booking"),
    path("booking/", views.booking_history, name = "booking_history"),
]