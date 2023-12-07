from web3 import Web3, HTTPProvider
from django.shortcuts import render, redirect
import json
import os

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
    contract_address = '0x64b2013eF2e08eA942b0F787cDa888A49645668c'

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

# Create a new ballot
def create_ballot(request):
    if request.method == 'POST':
        # Detect the user's MetaMask address
        if 'web3' in request.session:
            web3 = request.session['web3']
            from_address = web3.eth.defaultAccount
        else:
            # Handle the case where MetaMask is not connected
            return render(request, "error.html", {'message': 'Please connect your MetaMask wallet.'})

        max_choices = int(request.POST.get('max_choices'))
        options = [int(option) for option in request.POST.get('options').split(',')]

        try:
            # Initialize Web3 and the contract
            web3, contract = initialize_web3_and_contract()

            # Create a transaction object for the create_ballot function
            transaction = contract.functions.startVote(options, max_choices).buildTransaction({
                'from': from_address,
                'nonce': web3.eth.getTransactionCount(from_address),
                # Add other transaction parameters like gas, gasPrice, etc.
            })

            # Sign the transaction with MetaMask
            signed_transaction = web3.eth.account.signTransaction(transaction, private_key=None)  # Private key handled by MetaMask

            # Send the signed transaction to the Ethereum network
            transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            return redirect('home')

        except Exception as e:
            # Handle transaction errors and provide feedback to the user
            return render(request, "error.html", {'message': f'Transaction failed: {str(e)}'})

    # Handle other cases (GET request)
    # You can render a form for creating a new ballot here

    return render(request, "create_ballot.html", {'active_page': 'create_ballot'})