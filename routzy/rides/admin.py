from django.contrib import admin
from .models import Vehicle, Ride, Booking, ChatMessage

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Ride)
admin.site.register(Booking)
admin.site.register(ChatMessage)
