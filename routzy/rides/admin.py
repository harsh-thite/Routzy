from django.contrib import admin
from .models import Vehicle, Ride, Booking, Message

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Ride)
admin.site.register(Booking)
admin.site.register(Message)
