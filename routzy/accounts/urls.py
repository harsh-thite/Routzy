from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Login Page (using Django's built-in LoginView)
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Logout (using Django's built-in LogoutView)
    path('logout/', LogoutView.as_view(), name='logout'),  # Redirects based on LOGOUT_REDIRECT_URL

    # Signup Page (Custom Signup View)
    path('signup/', views.signup, name='signup'),

    # User Profile Page
    path('profile/', views.profile, name='profile'),
]
