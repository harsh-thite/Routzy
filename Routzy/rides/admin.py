from django.contrib import admin
from .models import User, Ride, Booking

admin.site.register(User)
admin.site.register(Ride)
admin.site.register(Booking)
