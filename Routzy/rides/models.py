from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ride(models.Model):
    VEHICLE_CHOICES = [
        ('Taxi', 'Taxi'),
        ('Bike', 'Bike'),
        ('Auto', 'Auto'),
        ('Car', 'Car'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    seats_available = models.IntegerField()
    cost_per_seat = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"

class Booking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.passenger.name} on {self.ride}"
