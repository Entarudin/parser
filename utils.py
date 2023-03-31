from hashlib import sha256
from uuid import UUID


def uuid_generate(string: str) -> UUID:
    hash_string = sha256(string.encode('utf-8'))
    return UUID(hash_string.hexdigest()[::2])
