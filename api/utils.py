import random
import string

def generate_random_string(length=4):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
