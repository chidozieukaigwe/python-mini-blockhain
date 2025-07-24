class Node:

    def __init__(self):
        self.blockchain = []

    def listen_for_input(self):

        waiting_for_input = True

        while waiting_for_input:

            print("Please choose")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("q: Quit")

            user_choice = self.get_user_choice()

            if user_choice == '1':
                # returns a tuple
                tx_data = self.get_transaction_value()
                # unpack tuple
                recipient, amount = tx_data
                if add_transaction(recipient=recipient, amount=amount):
                    print('Added transaction')
                else:
                    print('Failed to add transaction')
            elif user_choice == '2':
                if mine_block():
                    open_transactions = []
                    save_data()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(open_transactions, get_balance):
                    print('All transactions verified')
                else:
                    print('There are invalid transactions')
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print("Invalid choice")
            verifier = Verification()
            if not verifier.verify_chain(self.blockchain):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                break
            print('Balance of {}: {:6.2f}'.format('Chido', get_balance('Chido')))
        else:
            print("User Left")

        print('Done!')

    def get_transaction_value(self) -> tuple[str, float]:
        """
        Returns the input of the user (a new transaction amount) as a float
        :return: tuple[str, float]
        """
        # Get user input, transform it from string to a float and store it
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input("You transaction amount please: "))
        # this return statement returns a tuple
        return tx_recipient, tx_amount

    def get_user_choice(self) -> str:
        """
        Prompts the user for its choice and return it
        :return: str
        """
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self) -> None:
        """
        Out all blocks of the blockchain
        """
        # Output the blockchain list to the console
        for block in self.blockchain:
            print("Outputting Block")
            print(block)
        else:
            print('-' * 20)
