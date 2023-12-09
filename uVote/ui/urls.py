from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm


urlpatterns = [
    path("", views.root, name="root"),
    path("home", views.home, name="home"),
    path("vote", views.vote, name="vote"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'), 
    path('logout/', views.logout_view, name='logout'),
    path('please/', views.please, name='please'),
    path('submit_vote_options/', views.submit_vote_options, name='submit_vote_options'),
    path('get_voting_options/<int:vote_id>/', views.get_voting_options, name='get_voting_options'),
    path('get_vote_title/<int:vote_id>/', views.get_vote_title, name='get_vote_title'),
]