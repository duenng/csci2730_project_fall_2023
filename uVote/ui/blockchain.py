from web3 import Web3, HTTPProvider
import json
import os

def load_contract_abi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abi_path = os.path.join(dir_path, 'abi.json')
    with open(abi_path, 'r') as file:
        return json.load(file)

def initialize_web3_and_contract():
    web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
    contract_abi = load_contract_abi()
    contract_address = '0x64b2013eF2e08eA942b0F787cDa888A49645668c'
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    return web3, contract

def fetch_ballots(contract):
    next_ballot_id = contract.functions.nextBallotId().call()
    ballots = []
    for ballot_id in range(next_ballot_id):
        ballot_info = get_ballot_info(contract, ballot_id)
        ballots.append(ballot_info)
    return ballots

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

def submit_vote(web3, contract, from_address, ballot_id, selected_options):
    # Assumed that `selected_options` is a list of integers
    txn = contract.functions.castVote(ballot_id, selected_options).buildTransaction({
        'from': from_address,
        'nonce': web3.eth.getTransactionCount(from_address),
        # Add other transaction parameters like gas
    })
    # Sign and send the transaction. Requires the user's private key.
    # Private key handling should be done securely.

def create_ballot(web3, contract, from_address, options, max_choices):
    txn = contract.functions.startVote(options, max_choices).buildTransaction({
        'from': from_address,
        'nonce': web3.eth.getTransactionCount(from_address),
        # Add other transaction parameters like gas, gasPrice, etc.
    })
    # Sign and send the transaction. Requires the user's private key.
    # WARNING: Handle private keys with extreme caution and security.
    # signed_txn = web3.eth.account.signTransaction(txn, private_key)
    # txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # return txn_hash
