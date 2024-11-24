from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Ride, Booking
from rest_framework.viewsets import ModelViewSet
from .serializers import RideSerializer
from django.contrib import messages
from django.http import HttpResponseRedirect  # Add this import

User = get_user_model()  # Reference to the custom User model

# Home view (landing page)
def home(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        return redirect('rides_list')
    return render(request, 'home.html')


def login_view(request):
    # If user is already authenticated, redirect to home or another page
    if request.user.is_authenticated:
        print(f"User is already logged in: {request.user}")
        return redirect('home')  # or 'rides_list' or any other view

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Log the user in and create a session
            print(f"User logged in: {user}")  # Log to check user login

            # Ensure 'next' URL is provided, otherwise default to 'rides_list'
            next_url = request.POST.get('next', '') or 'rides_list'  # Default to 'rides_list' if 'next' is empty
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')  # Return to the login page with an error message

    # Capture the 'next' parameter from GET
    next_url = request.GET.get('next', '')  # If no next parameter is passed, it defaults to an empty string
    return render(request, 'login.html', {'next': next_url})


# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')


# Signup view
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})

        user = User.objects.create_user(username=email, email=email, password=password, name=name, phone=phone)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')


# Offer a Ride view
@login_required
def offer_ride(request):
    if request.method == "POST":
        start_location = request.POST.get('start_location')
        end_location = request.POST.get('end_location')
        vehicle_type = request.POST.get('vehicle_type')
        date_time = request.POST.get('date_time')
        seats_available = request.POST.get('seats_available')
        cost_per_seat = request.POST.get('cost_per_seat')

        Ride.objects.create(
            user=request.user,
            start_location=start_location,
            end_location=end_location,
            vehicle_type=vehicle_type,
            date_time=date_time,
            seats_available=seats_available,
            cost_per_seat=cost_per_seat
        )
        return redirect('rides_list')
    return render(request, 'offer_ride.html')


# List all available rides
@login_required
def rides_list(request):
    rides = Ride.objects.all()
    return render(request, 'rides_list.html', {'rides': rides})


# Book a ride
@login_required
def book_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    # Check if there are available seats
    if ride.seats_available > 0:
        if request.method == 'POST':
            # Reduce the available seats after booking
            ride.seats_available -= 1
            ride.save()

            # Redirect to the success page after booking
            return render(request, 'booking_success.html', {'ride': ride})

        # If it's a GET request, show the booking page
        return render(request, 'book_ride.html', {'ride': ride})
    else:
        # If no seats available, show the failure page
        return render(request, 'booking_failure.html', {'ride': ride})


# Filter rides based on location
def filter_rides(request):
    query = request.GET.get('query', '').strip()
    filtered_rides = Ride.objects.filter(
        start_location__icontains=query
    ) | Ride.objects.filter(end_location__icontains=query)

    html = render_to_string('partials/rides_list.html', {'rides': filtered_rides})
    return JsonResponse({'html': html})


# Chat Room
@login_required
def chat_room(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})


# API for Ride ViewSet
class RideViewSet(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
