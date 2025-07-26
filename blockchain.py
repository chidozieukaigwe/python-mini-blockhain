import functools
import json
from typing import Union, Any, Optional
# App
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

# Global Constant
MINING_REWARD = 10

class Blockchain:

    def __init__(self, hosting_node_id):
        # Initialize our blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        # unhandled transactions
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
        self.__peer_nodes = set()

    # Decorator acts as a get to the property
    @property
    def chain(self) -> list[Block]:
        # Return a copy of list not reference
        return self.__chain[:]

    @chain.setter
    def chain(self, value: list[Block]) -> None:
        self.__chain = value

    def get_open_transactions(self) -> list[Transaction]:
        return self.__open_transactions[:]

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
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]

                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
               pass
        finally:
            print('CleanUp!')

    def save_data(self):
        try:
            # write in binary data
            with open('blockchain.txt', mode='w') as file:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                # json dumps gives us back a string in JSON format
                file.write(json.dumps(saveable_chain))
                file.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                file.write(json.dumps(saveable_tx))
                file.write('\n')
                file.write(json.dumps(list(self.__peer_nodes)))

                # Integrate with Pickle
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # file.write(pickle.dumps(save_data))
        except IOError:
            print('Saving Failed')

    def proof_of_work(self) -> Union[int, Any]:
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self) -> Union[int, Any]:

        if self.hosting_node is None:
            return None

        participant = self.hosting_node
        # Fetch a list of all sent coin amounts for the given person (empty lists)
        # This fetches sent amounts of transactions that were already included in
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists)
        # This fetches sent amount of open transactions (to avoid double spending
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_sender, 0)
        # This fetches received coin amounts of transactions that were already in
        # We ignore open transactions here because you shouldn't be able to spend
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0 , tx_recipient, 0)
        # Return total balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self) -> Optional[Block]:
        """
        Returns the last value of the current blockchain
        :return: Optional[dict[str, Union[str, int, list[Any]]]]
        """
        # -1 gets the last value via its index
        if len(self.__chain) < 1:
            # None type: tells the program that there is nothing
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient: str, sender, signature,  amount: float = 1.0,) -> bool:
        """
        :param sender: The sender of coins
        :param recipient: The recipient of the coins
        :param signature: The signature of the transaction
        :param amount: The amount of coins sent with the transaction (default = 1.0)
        :return: bool
        """

        if self.hosting_node is None:
            return False

        transaction = Transaction(sender=sender, recipient=recipient, signature=signature, amount=amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """
        Create a new block and add open transactions to it
        :return: bool
        """

        if self.hosting_node is None:
            return None

        # Fetch the currently last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        # Miners are rewarded via reward transaction
        reward_transaction = Transaction(sender='MINING', recipient=self.hosting_node, signature='', amount=MINING_REWARD)

        # Copying transaction instead of manipulating the original open_transactions list [:] means to copy complete list
        # This ensures that if for some reason the mining should fail, we dont have the reward transaction
        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None

        copied_transactions.append(reward_transaction)

        block = Block(len(self.__chain), hashed_block,copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self, node):
        """ Add a new node to the peer node set

            Arguments:
                :node: The node URL which be added
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """ Remove a node from the peer node set

        Arguments:
              :node: The node URL which will be removed
        """
        self.__peer_nodes.discard(node)
        self.save_data()