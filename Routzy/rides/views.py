from django.shortcuts import render, redirect
from .models import User, Ride, Booking
from django.contrib.auth.hashers import make_password, check_password


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
def offer_ride(request):
    if request.method == "POST":
        # Handle form submission for offering a ride
        pass
    return render(request, 'offer_ride.html')

# List available rides
def rides_list(request):
    rides = Ride.objects.all()
    return render(request, 'rides_list.html', {'rides': rides})

# Book a ride
def book_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    # Handle ride booking logic here
    return redirect('rides_list')
