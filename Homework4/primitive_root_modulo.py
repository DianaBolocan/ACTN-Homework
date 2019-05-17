import random


def is_prime(number):
    for index in range(2, int(number / 2)):
        if number % index == 0:
            return False
    return True


def generate(p=None, limit=None):
    if not limit:
        limit = pow(2, 32)
    if not p or not is_prime(p):
        r = random.randint(2, limit)
        while not is_prime(r):
            r = random.randint(2, limit)
        p = 2 * r + 1
    number = random.randint(2, (p - 1) / 2)
    return -(pow(number, 2, p)) % p, p


if __name__ == '__main__':
    primitive_root, prime = generate()
    print("Primitive root: {}\nPrime number: {}".format(primitive_root, prime))
