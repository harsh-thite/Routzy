from django import forms
from .models import Ride, Vehicle, Message

class RideOfferForm(forms.ModelForm):
    departure_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Ride
        fields = ['start_location', 'end_location', 'departure_time', 'total_seats', 'cost_per_seat']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['type', 'model', 'registration_number']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']