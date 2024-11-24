from django.shortcuts import render, redirect
from .models import User, Ride, Booking
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


# Home view (landing page)
def home(request):
    return render(request, 'home.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect('rides_list')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Add this function to handle logout
def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        hashed_password = make_password(password)
        User.objects.create(name=name, email=email, phone=phone, password=hashed_password)
        return redirect('login')
    return render(request, 'signup.html')

# Offer Ride view
@login_required
def offer_ride(request):
    if request.method == "POST":
        start_location = request.POST.get('start_location')
        end_location = request.POST.get('end_location')
        vehicle_type = request.POST.get('vehicle_type')
        date_time = request.POST.get('date_time')
        seats_available = request.POST.get('seats_available')
        cost_per_seat = request.POST.get('cost_per_seat')

        # Unwrap the SimpleLazyObject to get the actual user instance
        user = User.objects.get(pk=request.user.id)

        Ride.objects.create(
            user=user,
            start_location=start_location,
            end_location=end_location,
            vehicle_type=vehicle_type,
            date_time=date_time,
            seats_available=seats_available,
            cost_per_seat=cost_per_seat
        )
        return redirect('rides_list')  # Redirect to Available Rides page
    return render(request, 'offer_ride.html')

# List available rides
def rides_list(request):
    rides = Ride.objects.all()  # Query all rides
    return render(request, 'rides_list.html', {'rides': rides})

# Book a ride
def book_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    # Handle ride booking logic here
    return redirect('rides_list')


def filter_rides(request):
    query = request.GET.get('query', '').strip()
    filtered_rides = Ride.objects.filter(
        start_location__icontains=query
    ) | Ride.objects.filter(end_location__icontains=query)

    html = render_to_string('partials/rides_list.html', {'rides': filtered_rides})
    return JsonResponse({'html': html})

def chat_room(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})
