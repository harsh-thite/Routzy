from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import RideViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('offer_ride/', views.offer_ride, name='offer_ride'),
    path('rides/', views.rides_list, name='rides_list'),
    path('book_ride/<int:ride_id>/', views.book_ride, name='book_ride'),
    path('filter_rides/', views.filter_rides, name='filter_rides'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]
