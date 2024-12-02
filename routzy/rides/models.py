from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('CAR', 'Car'),
        ('BIKE', 'Bike'),
        ('TAXI', 'Taxi'),
        ('CAB', 'Cab'),
        ('AUTO', 'Auto Rickshaw')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.model}"


class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offered_rides')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)

    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)

    departure_time = models.DateTimeField()
    total_seats = models.IntegerField(default=4)
    available_seats = models.IntegerField(default=4)
    cost_per_seat = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('FULL', 'Full'),
        ('COMPLETED', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_location} to {self.end_location} by {self.driver.username}"


class RideBooking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    seats_booked = models.IntegerField(default=1)
    booking_time = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')

    def __str__(self):
        return f"{self.passenger.username} - {self.ride}"


class ChatMessage(models.Model):
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message by {self.sender.username} on Ride {self.ride.id}"