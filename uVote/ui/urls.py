from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("home", views.home, name="home"),
    path("vote", views.vote, name="vote"),
]