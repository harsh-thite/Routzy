from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .models import ChatMessage
from .forms import ChatMessageForm

# Use apps.get_model when referencing Ride
Ride = apps.get_model('rides', 'Ride')

@login_required
def ride_chat(request, ride_id):
    """View to display and handle chat messages for a specific ride."""
    ride = get_object_or_404(Ride, id=ride_id)

    # Check if the user is allowed to access the chat
    if ride.driver != request.user and not ride.bookings.filter(passenger=request.user).exists():
        return redirect('available_rides')  # Redirect if the user is not involved in the ride

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.ride = ride
            chat_message.sender = request.user
            chat_message.save()
            return redirect('ride_chat', ride_id=ride.id)
    else:
        form = ChatMessageForm()

    messages = ride.chat_messages.all()  # Fetch chat messages for the ride
    return render(request, 'chat/ride_chat.html', {'ride': ride, 'messages': messages, 'form': form})