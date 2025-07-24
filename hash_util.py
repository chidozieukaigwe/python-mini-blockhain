import hashlib as hl
import json

def hash_string_256(value) -> str:
    """
    Hash a string using sha256
    :param value:
    :return: str
    """
    return hl.sha256(value).hexdigest()

def hash_block(block) -> str:
    """
    Hashes a block and returns a string representation of the block
    :param block:
    :return: string representation of the block
    """
    return hash_string_256(json.dumps(block, sort_keys=True).encode())