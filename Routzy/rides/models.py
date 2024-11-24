from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # For dynamic User model reference


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.username


class Ride(models.Model):
    VEHICLE_CHOICES = [
        ('Taxi', 'Taxi'),
        ('Bike', 'Bike'),
        ('Auto', 'Auto'),
        ('Car', 'Car'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ride creator
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES)
    date_time = models.DateTimeField()
    seats_available = models.PositiveIntegerField()
    cost_per_seat = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.start_location} to {self.end_location} on {self.date_time}"


class Booking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.passenger.username} on {self.ride}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
