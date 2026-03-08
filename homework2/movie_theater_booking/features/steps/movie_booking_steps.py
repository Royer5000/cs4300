from behave import given, when, then
from django.test import Client
from bookings.models import Movie, Seat, Booking

client = Client()
response = None
movie = None

@given("there is a movie")
def step_create_movie(context):
    context.movie = Movie.objects.create(
        title = "Edge of Tomorrow",
        description = "Tom Cruise time travel",
        release_date = "2014-05-28",
        duration = 113
    )


@given("there is an available seat")
def step_create_available_seat(context):
    context.seat = Seat.objects.create(
        seat_number = "3",
        booking_status = False
    )


@when("I select an available seat")
def step_select_available_seat(context):
    context.response = context.client.post(
        f"/book/{context.movie.id}/",
        {
            "user" : "Jayden",
            "seat_number" : "3"
        },
        follow = True
    )


@then("that seat should be booked")
def step_check_seat_booked(context):
    seat = Seat.objects.get(seat_number = "3")
    assert seat.booking_status is True

    booking = Booking.objects.filter(
        user = "Jayden",
        seat = "3",
        movie = "Edge of Tomorrow"
    ).exists()
    assert booking is True