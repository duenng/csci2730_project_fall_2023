from web3 import Web3, HTTPProvider
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VotingOption
import os

def get_vote_title(request, vote_id):
    try:
        vote_options = VotingOption.objects.filter(vote_id=vote_id)
        if vote_options.exists():
            vote_title = vote_options.first().vote_title  # Assuming 'vote_title' is a field in your model
            return JsonResponse({'title': vote_title})
        else:
            return JsonResponse({'title': 'Unknown Vote'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_voting_options(request, vote_id):
    try:
        options = VotingOption.objects.filter(vote_id=vote_id).values('option_number', 'option_name')
        return JsonResponse(list(options), safe=False)
    except Exception as e:
        # Log the exception for debugging
        print(f"Error fetching voting options: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def submit_vote_options(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            options_data = data['optionsData']
            vote_id = data['voteId']  # Capture the vote ID
            vote_title = data['voteTitle'] 
            # Process and save each option with the vote ID
            for option in options_data:
                VotingOption.objects.create(
                    vote_id=vote_id,
                    vote_title= vote_title,
                    option_number=option['number'],
                    option_name=option['name']
                )
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'invalid request'}, status=400)

# Load the contract ABI from a JSON file
def load_contract_abi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abi_path = os.path.join(dir_path, 'abi.json')
    with open(abi_path, 'r') as file:
        return json.load(file)

# Initialize Web3 and the contract
def initialize_web3_and_contract():
    # Connect to a local Ethereum node (replace with your actual node URL)
    web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

    # Load the contract ABI from the JSON file
    contract_abi = load_contract_abi()

    # Replace with your contract address
    contract_address = '0x5c1612f3d8b2eB23537f92A85616A063b6bD13AF'

    # Create a contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return web3, contract

# Fetch information about all ballots
def fetch_ballots(contract):
    next_ballot_id = contract.functions.nextBallotId().call()
    ballots = []
    for ballot_id in range(next_ballot_id):
        ballot_info = get_ballot_info(contract, ballot_id)
        ballots.append(ballot_info)
    return ballots

# Get information about a specific ballot
def get_ballot_info(contract, ballot_id):
    is_open = contract.functions.isVotingOpen(ballot_id).call()
    max_choices = contract.functions.getMaxChoices(ballot_id).call()
    # Additional ballot info can be added here
    return {
        'id': ballot_id,
        'is_open': is_open,
        'max_choices': max_choices,
        # Add more information as needed
    }

# Submit a vote for a specific ballot
def submit_vote(web3, contract, from_address, ballot_id, selected_options):
    # Assumed that `selected_options` is a list of integers
    txn = contract.functions.castVote(ballot_id, selected_options).buildTransaction({
        'from': from_address,
        'nonce': web3.eth.getTransactionCount(from_address),
        # Add other transaction parameters like gas
    })
    # Sign and send the transaction. Requires the user's private key.
    # Private key handling should be done securely.
