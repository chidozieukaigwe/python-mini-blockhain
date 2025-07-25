from Crypto.PublicKey import RSA
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

    def load_key(self):
        pass

    @staticmethod
    def __generate_keys():
       private_key = RSA.generate(1024, Crypto.Random.new().read)
       public_key = private_key.publickey()
       # convert binary into a string
       return binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')