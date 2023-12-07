from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path("", views.root, name="root"),
    path("home", views.home, name="home"),
    path("vote", views.vote, name="vote"),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('register/', views.register_view, name='register'), 
]