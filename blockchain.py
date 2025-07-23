import functools
# Global Constant
MINING_REWARD = 10

# Initialize our blockchain list
genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
}
blockchain = [genesis_block]  #python list
open_transactions = []
owner = 'Chido'
# initializes a set as we did not add key value paring that would turn it into a dictionary
participants = {'Chido'}

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def get_balance(participant: str):
    # nest list comprehension
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 20 , tx_recipient, 0)
    return amount_received - amount_sent

def get_last_blockchain_value():
    # -1 gets the last value via its index
    if len(blockchain) < 1:
        # None type: tells the program that there is nothing
        return None
    return blockchain[-1]


def get_transaction_value():
    # Get user input, transform it from string to a float and store it
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input("You transaction amount please: "))
    # this return statement returns a tuple
    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    # Output the blockchain list to the console
    for block in blockchain:
        print("Outputting Block")
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    # enumerate: give you back a tuple with two pieces of info - index:element
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False

    return True

def verify_transactions():
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

def mine_block():
    last_block = blockchain[-1]
    #  list comprehension - creates a list for every value of the incoming dictionary
    #  Wrap list to turn it into string
    hashed_block = hash_block(last_block)
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
