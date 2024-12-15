from django.urls import path
from . import views

urlpatterns = [
    path('available-rides/', views.available_rides, name='available_rides'),
    path('offer-ride/', views.offer_ride, name='offer_ride'),
    path('my-rides/', views.my_rides, name='my_rides'),
    path('ride-details/<int:ride_id>/', views.ride_details, name='ride_details'),
    path('book-ride/<int:ride_id>/', views.book_ride, name='book_ride'),  # NEW
]