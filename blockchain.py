import functools
import json
import pickle # convert python data to binary in a file
from typing import Union, Any, Optional
from uuid import  uuid4
# App
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

# Global Constant
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id: uuid4)-> None:
        # Initialize our blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        # unhandled transactions
        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as file:
                # give use all the lines in a list readlines() fn
                file_content = file.readlines()

                # When using pickle
                # file_content = pickle.loads(file.read())

                # Integrate With Pickle
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']

                # [:-1] range remove the last char =\n
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]

                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp']
                    )

                updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        except (IOError, IndexError):
               pass
        finally:
            print('CleanUp!')

    def save_data(self):
        try:
            # write in binary data
            with open('blockchain.txt', mode='w') as file:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.chain]]
                # json dumps gives us back a string in JSON format
                file.write(json.dumps(saveable_chain))
                file.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                file.write(json.dumps(saveable_tx))

                # Integrate with Pickle
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # file.write(pickle.dumps(save_data))
        except IOError:
            print('Saving Failed')

    def proof_of_work(self) -> Union[int, Any]:
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self) -> Union[int, Any]:
        participant = self.hosting_node
        # Fetch a list of all sent coin amounts for the given person (empty lists)
        # This fetches sent amounts of transactions that were already included in
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists)
        # This fetches sent amount of open transactions (to avoid double spending
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_sender, 0)
        # This fetches received coin amounts of transactions that were already in
        # We ignore open transactions here because you shouldn't be able to spend
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_recipient, 0)
        # Return total balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self) -> Optional[dict[str, Union[str, int, list[Any]]]]:
        """
        Returns the last value of the current blockchain
        :return: Optional[dict[str, Union[str, int, list[Any]]]]
        """
        # -1 gets the last value via its index
        if len(self.chain) < 1:
            # None type: tells the program that there is nothing
            return None
        return self.chain[-1]

    def add_transaction(self, recipient: str, sender: uuid4, amount: float = 1.0) -> bool:
        """
        :param sender: The sender of coins
        :param recipient: The recipient of the coins
        :param amount: The amount of coins sent with the transaction (default = 1.0)
        :return: bool
        """
        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self) -> bool:
        """
        Create a new block and add open transactions to it
        :return: bool
        """
        # Fetch the currently last block of the blockchain
        last_block = self.chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        # Miners are rewarded via reward transaction
        reward_transaction = Transaction(sender='MINING', recipient=self.hosting_node, amount=MINING_REWARD)

        # Copying transaction instead of manipulating the original open_transactions list [:] means to copy complete list
        # This ensures that if for some reason the mining should fail, we dont have the reward transaction
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        block = Block(len(self.chain), hashed_block,copied_transactions, proof)

        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True




