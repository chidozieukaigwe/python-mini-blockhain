import hashlib as hl
from block import Block
import json

# Export only the functions listed in the list
# __all__ = ['hash_string_256', 'hash_block']

def hash_string_256(value) -> str:
    """
    Hash a string using sha256
    :param value:
    :return: str
    """
    return hl.sha256(value).hexdigest()

def hash_block(block: Block) -> str:
    """
    Hashes a block and returns a string representation of the block
    :param block:
    :return: string representation of the block
    """
    # Convert Block class to a dict data type + copy the block instance
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] =  [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())