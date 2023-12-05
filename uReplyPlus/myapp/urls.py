from django.urls import path
from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("home", views.home, name="home"),
    path("attendance", views.attendance, name="attendance"),
    path("qa", views.qa, name="qa"),
    path("vote", views.vote, name="vote"),
]