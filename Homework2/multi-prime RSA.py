import sympy, sys


def generate_pqr_primes():
    q = None
    r = None
    p = sympy.randprime(pow(2, 512), pow(2, 523))
    while q is None:
        q = sympy.randprime(pow(2, 512), pow(2, 523))
        if q == p:
            q = None
    while r is None:
        r = sympy.randprime(pow(2, 512), pow(2, 523))
        if r == p or r == q:
            r = None
    return p, q, r


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def get_message(path):
    with open(path, "rb") as fd:
        message = fd.read()
    return message


def encrypt_message(path, n):
    message = get_message(path)
    message = int.from_bytes(message, byteorder=sys.byteorder)
    encrypted = pow(message, e, n)
    with open("cryptotext.txt", "w") as fd:
        fd.write(str(encrypted))
    return encrypted


def garner(y, d, p, q, r):
    return


p, q, r = generate_pqr_primes()
e = pow(2, 16) + 1
n = p * q * r
phi_n = (p - 1) * (q - 1) * (r - 1)
condition = gcd(e, phi_n)
while condition != 1:
    p, q, r = generate_pqr_primes()
    n = p * q * r
    phi_n = (p - 1) * (q - 1) * (r - 1)
    condition(e, phi_n)
d = sympy.mod_inverse(e, phi_n)
y = encrypt_message("message.txt", n)
print("p:", p)
print("q:", q)
print("r:", r)
print("e:", e)
print("d:", d)
print("m:", int.from_bytes(get_message(path="message.txt"), byteorder=sys.byteorder))
print("y:", y)
print("y decrypted with python library:", pow(y, d, n))
print("y decrypted with Garner:", garner())
