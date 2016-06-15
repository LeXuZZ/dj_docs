import random
import string


def generate_hash(hash_length: int) -> str:
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase
    ) for _ in range(hash_length))

