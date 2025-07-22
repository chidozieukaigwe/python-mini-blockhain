# Initialize our blockchain list
blockchain = [] #python list

def get_last_blockchain_value():
    # -1 gets the last value via its index
    if len(blockchain) < 1:
        # None type: tells the program that there is nothing
        return None
    return blockchain[-1]

def get_transaction_value():
    user_input = float(input("Enter a value for the blockchain: "))
    return user_input

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
    # block_index = 0
    is_valid = True
    # verify if current block is equal to previous block in chain
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid

def add_transaction(transaction_amount: float, last_transaction=[1]):
    if last_transaction is None:
        last_transaction = [1]
    blockchain.append( [ last_transaction, transaction_amount])

# keyword arguments example
# add_value(last_transaction=get_last_blockchain_value(), transaction_amount=tx_amount)

waiting_for_input = True

while waiting_for_input:

    print("Please choose")
    print("1: Add a new transaction")
    print("2: Output the blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")

    user_choice = get_user_choice()

    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = 2
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Invalid choice")
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain!")
        break
else:
    print("User Left")

print('Done!')