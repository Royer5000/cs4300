Feature: Movie Seat Booking

    Scenario: User Books a Movie Seat
        Given there is a movie
        And there is an available seat
        When I select an available seat
        Then that seat should be booked