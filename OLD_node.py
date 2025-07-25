from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:

    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def listen_for_input(self):

        waiting_for_input = True

        while waiting_for_input:

            print("Please choose")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("5: Create Wallet")
            print("6: Load Wallet")
            print("7: Save Wallet Keys")
            print("q: Quit")

            user_choice = self.get_user_choice()

            if user_choice == '1':
                # returns a tuple
                tx_data = self.get_transaction_value()
                # unpack tuple
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient=recipient, sender=self.wallet.public_key, signature=signature, amount=amount):
                    print('Added transaction')
                else:
                    print('Failed to add transaction')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed, have you created a wallet')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions verified')
                else:
                    print('There are invalid transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print("Invalid choice")
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                break
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
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
        for block in self.blockchain.chain:
            print("Outputting Block")
            print(block)
        else:
            print('-' * 20)

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

