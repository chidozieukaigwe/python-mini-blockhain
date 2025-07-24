from hash_util import hash_string_256, hash_block
from transaction import Transaction
class Verification:

    def verify_chain(self, blockchain) -> bool:
        """
        Verify the current blockchain and return True it its valid, False otherwise
        :return: bool
        """
        # enumerate: give you back a tuple with two pieces of info - index:element
        for (index, block) in enumerate(blockchain.chain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain.chain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True

    def verify_transaction(self,transaction: Transaction, get_balance):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    def verify_transactions(self, open_transactions, get_balance) -> bool:
        """
        Verifies all open transactions
        :return: bool
        """
        # Check all transactions in one go via the all function and list comprehension
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])

    def valid_proof(self, transactions: list, last_hash: str, proof: int) -> bool:
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