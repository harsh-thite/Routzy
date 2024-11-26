from django.contrib import admin
from .models import Vehicle, Ride, RideBooking

admin.site.register(Vehicle)
admin.site.register(Ride)
admin.site.register(RideBooking)