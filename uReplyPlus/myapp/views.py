from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def home(request):
    return render(request, "home.html")

def qa(request):
    return render(request, "qa.html")

def vote(request):
    return render(request, "vote.html")

def attendance(request):
    return render(request, "attendance.html")

def root(request):
    return redirect('home')