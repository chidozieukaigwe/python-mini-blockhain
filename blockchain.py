import functools
import hashlib as hl
import json
from typing import Union, Any, Optional

# Global Constant
MINING_REWARD = 10

# Initialize our blockchain
genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
    "proof": 100
}
# Initializing our (empty) blockchain list
blockchain = [genesis_block]
# unhandled transactions
open_transactions = []
# We are the owner of this blockchain node, hence this is our ID
owner = 'Chido'
# Registered participants: Ourselves + other people sending / receiving coins
participants = {'Chido'}

def hash_block(block: dict):
    """
    Hashes a block and returns a string representation of the block
    :param block:
    :return: string representation of the block
    """
    return hl.sha256(json.dumps(block).encode()).hexdigest()

def valid_proof(transactions: list, last_hash: str, proof: int):
    """
    Validate the proof of work when mining a block
    :param transactions:
    :param last_hash:
    :param proof:
    :return: bool
    """
    guess: bytes = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work() -> Union[int, Any]:
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def get_balance(participant: str) -> Union[int, Any]:
    # Fetch a list of all sent coin amounts for the given person (empty lists)
    # This fetches sent amounts of transactions that were already included in
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    # Fetch a list of all sent coin amounts for the given person (empty lists)
    # This fetches sent amount of open transactions (to avoid double spending
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_sender, 0)
    # This fetches received coin amounts of transactions that were already in
    # We ignore open transactions here because you shouldnt be able to spend
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_recipient, 0)
    # Return total balance
    return amount_received - amount_sent

def get_last_blockchain_value() -> Optional[dict[str, Union[str, int, list[Any]]]]:
    """
    Returns the last value of the current blockchain
    :return: Optional[dict[str, Union[str, int, list[Any]]]]
    """
    # -1 gets the last value via its index
    if len(blockchain) < 1:
        # None type: tells the program that there is nothing
        return None
    return blockchain[-1]


def get_transaction_value() -> tuple[str, float]:
    """
    Returns the input of the user (a new transaction amount) as a float
    :return: tuple[str, float]
    """
    # Get user input, transform it from string to a float and store it
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input("You transaction amount please: "))
    # this return statement returns a tuple
    return tx_recipient, tx_amount


def get_user_choice() -> str:
    """
    Prompts the user for its choice and return it
    :return: str
    """
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements() -> None:
    """
    Out all blocks of the blockchain
    """
    # Output the blockchain list to the console
    for block in blockchain:
        print("Outputting Block")
        print(block)
    else:
        print('-' * 20)


def verify_chain() -> bool:
    """
    Verify the current blockchain and return True it its valid, False otherwise
    :return: bool
    """
    # enumerate: give you back a tuple with two pieces of info - index:element
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True

def verify_transactions() -> bool:
    """
    Verifies all open transactions
    :return: bool
    """
    # Check all transactions in one go via the all function and list comprehension
    return all([verify_transaction(tx) for tx in open_transactions])

def verify_transaction(transaction: dict):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def add_transaction(recipient: str, sender: str = owner, amount: float = 1.0) -> bool:
    """
    :param sender: The sender of coins
    :param recipient: The recipient of the coins
    :param amount: The amount of coins sent with the transaction (default = 1.0)
    :return: bool
    """
    transaction: dict = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def mine_block() -> bool:
    """
    Create a new block and add open transactions to it
    :return: bool
    """
    # Fetch the currently last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block (=> to be able to compare it to the stored hash value
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # Miners are rewarded via reward transaction
    reward_transaction: dict = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block: dict = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True

# keyword arguments example
# add_value(last_transaction=get_last_blockchain_value(), transaction_amount=tx_amount)

waiting_for_input = True

while waiting_for_input:

    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print("q: Quit")

    user_choice = get_user_choice()

    if user_choice == '1':
        # returns a tuple
        tx_data = get_transaction_value()
        # unpack tuple
        recipient, amount = tx_data
        if add_transaction(recipient=recipient, amount=amount):
            print('Added transaction')
        else:
            print('Failed to add transaction')
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Sam', 'recipient': 'Chido', 'amount': 1, }]
            }
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions verified')
        else:
            print('There are invalid transactions')
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Invalid choice")
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain!")
        break
    print('Balance of {}: {:6.2f}'.format('Chido', get_balance('Chido')))
else:
    print("User Left")

print('Done!')
