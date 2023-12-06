from django.shortcuts import render, redirect
from web3 import Web3
import json

def home(request):
    return render(request, "home.html")

def vote(request):
    web3, contract = initialize_web3_and_contract()  # Initialize here
    ballots = fetch_ballots(contract)

    if request.method == 'POST':
        # ... handle the vote submission ...
        return redirect('home')

    return render(request, "vote.html", {"ballots": ballots})

def root(request):
    return redirect('home')

def load_contract_abi():
    with open('../ui/abi.json', 'r') as file:
        return json.load(file)

def initialize_web3_and_contract():
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Update this with your provider URL
    
    # Contract ABI
    
    contract_abi_string = '''
    [
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                },
                {
                    "indexed": false,
                    "internalType": "uint256[]",
                    "name": "optionCounts",
                    "type": "uint256[]"
                }
            ],
            "name": "VoteEnded",
            "type": "event"
        },
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                }
            ],
            "name": "VoteStarted",
            "type": "event"
        },
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "voter",
                    "type": "address"
                },
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                },
                {
                    "indexed": false,
                    "internalType": "uint256[]",
                    "name": "selectedOptions",
                    "type": "uint256[]"
                }
            ],
            "name": "Voted",
            "type": "event"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256[]",
                    "name": "selectedOptions",
                    "type": "uint256[]"
                }
            ],
            "name": "castVote",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                }
            ],
            "name": "getMaxChoices",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "option",
                    "type": "uint256"
                }
            ],
            "name": "getOptionCount",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "voter",
                    "type": "address"
                }
            ],
            "name": "hasVoted",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                }
            ],
            "name": "isVotingOpen",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "nextBallotId",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256[]",
                    "name": "_options",
                    "type": "uint256[]"
                },
                {
                    "internalType": "uint256",
                    "name": "_maxChoices",
                    "type": "uint256"
                }
            ],
            "name": "startVote",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "ballotId",
                    "type": "uint256"
                }
            ],
            "name": "tallyVotes",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    '''
    
    contract_abi = json.loads(contract_abi_string)

    # Contract Address
    contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'  # Replace with your contract's address

    # Creating a contract object
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return web3, contract

def fetch_ballots(contract):
    # ... fetch ballots logic ...
    pass

def submit_vote(ballot_id, selected_options, contract):
    # ... submit vote logic ...
    pass
