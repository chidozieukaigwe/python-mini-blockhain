""" Provides verification helper methods """

from utility.hash_util import hash_string_256, hash_block
from transaction import Transaction
from wallet import Wallet
class Verification:

    @classmethod
    def verify_chain(cls, blockchain) -> bool:
        """
        A helper class which offers various static and class based verification methods
        :return: bool
        """
        # enumerate: give you back a tuple with two pieces of info - index:element
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction: Transaction, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance) -> bool:
        """
        Verifies all open transactions
        :return: bool
        """
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])

    @staticmethod
    def valid_proof(transactions: list, last_hash: str, proof: int) -> bool:
        """
        Validate the proof of work when mining a block
        :param transactions:
        :param last_hash:
        :param proof:
        :return: bool
        """
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'