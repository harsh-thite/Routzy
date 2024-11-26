from django import forms
from .models import Ride, Vehicle, ChatMessage

class RideOfferForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['start_location', 'end_location', 'departure_time', 'total_seats', 'cost_per_seat']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['type', 'model', 'registration_number']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
