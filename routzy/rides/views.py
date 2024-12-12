from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehicle, Ride, Booking
from .forms import RideOfferForm, VehicleForm, ChatMessageForm
from django.contrib import messages

@login_required
def offer_ride(request):
    if request.method == 'POST':
        ride_form = RideOfferForm(request.POST)
        vehicle_form = VehicleForm(request.POST)
        if ride_form.is_valid() and vehicle_form.is_valid():
            vehicle = vehicle_form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            ride = ride_form.save(commit=False)
            ride.driver = request.user
            ride.vehicle = vehicle
            ride.save()
            return redirect('available_rides')
    else:
        ride_form = RideOfferForm()
        vehicle_form = VehicleForm()
    return render(request, 'rides/offer_ride.html', {'ride_form': ride_form, 'vehicle_form': vehicle_form})

def available_rides(request):
    rides = Ride.objects.filter(status='OPEN')
    return render(request, 'rides/available_rides.html', {'rides': rides})

@login_required
def ride_details(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    if request.method == 'POST':
        message_form = ChatMessageForm(request.POST)
        if message_form.is_valid():
            chat_message = message_form.save(commit=False)
            chat_message.ride = ride
            chat_message.sender = request.user
            chat_message.save()
            return redirect('ride_details', ride_id=ride.id)
    else:
        message_form = ChatMessageForm()
    messages = ride.messages.all()
    return render(request, 'rides/ride_details.html', {'ride': ride, 'messages': messages, 'message_form': message_form})

@login_required
def book_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    if ride.available_seats > 0:
        Booking.objects.create(user=request.user, ride=ride)
        ride.available_seats -= 1
        ride.save()
        messages.success(request, "Ride booked successfully!")
    else:
        messages.error(request, "No available seats for this ride.")
    return redirect('available_rides')

@login_required
def my_rides(request):
    offered_rides = request.user.offered_rides.all()
    booked_rides = RideBooking.objects.filter(passenger=request.user)
    return render(request, 'rides/my_rides.html', {'offered_rides': offered_rides, 'booked_rides': booked_rides})

def ride_chat(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)  # Get the Ride object
    chat_messages = ChatMessage.objects.filter(ride_id=ride_id).order_by('timestamp')  # Fetch chat messages for this ride

    return render(request, 'rides/ride_chat.html', {
        'ride': ride,
        'chat_messages': chat_messages
    })