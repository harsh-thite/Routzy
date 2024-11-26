from django.urls import path
from . import views

urlpatterns = [
    path('offer/', views.offer_ride, name='offer_ride'),
    path('available/', views.available_rides, name='available_rides'),
    path('details/<int:ride_id>/', views.ride_details, name='ride_details'),
    path('book/<int:ride_id>/', views.book_ride, name='book_ride'),
    path('my-rides/', views.my_rides, name='my_rides'),
    path('ride/<int:ride_id>/chat/', views.ride_chat, name='ride_chat'),
]