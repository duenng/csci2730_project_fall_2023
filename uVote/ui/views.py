from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from web3 import Web3
from .blockchain import *
from .forms import CustomUserCreationForm
from django.http import JsonResponse

def home(request):
    return render(request, "home.html", {'active_page': 'home'})

def vote(request):
    if not request.user.is_authenticated:
        # Return a response that triggers a JavaScript alert
        return render(request, "registration/please.html")

    web3, contract = initialize_web3_and_contract()
    ballots = fetch_ballots(contract)

    if request.method == 'POST':
        # Extract form data, such as ballot_id and selected_options
        # You also need the user's Ethereum address and private key for transaction signing
        from_address = request.POST.get('from_address')
        ballot_id = int(request.POST.get('ballot_id'))
        selected_options = request.POST.getlist('options')  # Assumed to be a list of option IDs

        # Convert option IDs to integers
        selected_options = [int(option) for option in selected_options]

        # Call submit_vote
        submit_vote(web3, contract, from_address, ballot_id, selected_options)
        
        return redirect('home')

    return render(request, "vote.html", {"ballots": ballots, 'active_page': 'vote'})


def root(request):
    return redirect('home')

def please(request):
    return render(request, "please.html")

def logout_view(request):
    logout(request)
    return redirect('home') 

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form, 'active_page': 'register'})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page.
            else:
                # Return an 'invalid login' error message
                form.add_error(None, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form, 'active_page': 'login'})
