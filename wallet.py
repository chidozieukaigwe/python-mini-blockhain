from typing import Optional
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

class Wallet:
    def __init__(self):

        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.__generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as file:
                keys = file.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
            return True
        except (IOError, IndexError):
            print('Loading wallet failed')
            return False

    def save_keys(self)-> Optional[bool]:
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('wallet.txt', mode='w') as file:
                    file.write(self.public_key)
                    file.write('\n')
                    file.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Saving wallet failed')
                return False
        return None

    @staticmethod
    def __generate_keys():
       private_key = RSA.generate(1024, Crypto.Random.new().read)
       public_key = private_key.publickey()
       # convert binary into a string
       return binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')

    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):

        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))

        verifier = PKCS1_v1_5.new(public_key)

        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))

        return verifier.verify(h, binascii.unhexlify(transaction.signature))
