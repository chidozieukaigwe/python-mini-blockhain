from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    """A transaction which can be added to a block in the blockchain

    Attributes:
        :sender: The sender of the transaction
        :recipient: The recipient of the transaction
        :signature: The signature of the transaction
        :amount: The amount of the transaction
    """
    def __init__(self, sender, recipient, signature, amount ):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient),('amount', self.amount),])

