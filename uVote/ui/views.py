from django.shortcuts import render, redirect
from web3 import Web3
from .blockchain import *
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, "home.html")

def vote(request):
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

    return render(request, "vote.html", {"ballots": ballots})

def root(request):
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect('login')  # Assuming you have a 'login' URL pattern
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})