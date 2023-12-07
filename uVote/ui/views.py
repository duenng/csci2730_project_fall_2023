from django.shortcuts import render, redirect
from .blockchain_view import *
from .auth_view import *

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
