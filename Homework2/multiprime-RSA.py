import sympy, sys, time


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


def encrypt_message(path, n, e):
    message = get_message(path)
    message = int.from_bytes(message, byteorder=sys.byteorder)
    encrypted = pow(message, e, n)
    with open("cryptotext.txt", "w") as fd:
        fd.write(str(encrypted))
    return encrypted


def garner(y, d, p, q, r):
    start = time.time()
    mp = pow(y % p, d % (p - 1), p)
    mq = pow(y % q, d % (q - 1), q)
    mr = pow(y % r, d % (r - 1), r)
    x = mp
    alpha = (((mq - x) % q) * sympy.mod_inverse(mp, q)) % q
    x += alpha * mp
    alpha = (((mr - x) % r) * sympy.mod_inverse(mp * mq, r)) % r
    x += alpha * mp * mq
    end = time.time() - start
    return x, end


def decrypt(y, d, n):
    start = time.time()
    x = pow(y, d, n)
    end = time.time() - start
    return x, end


def multiprime_RSA(iterations=10):
    average_time = 0
    for iteration in range(iterations):
        print("Iteration:", iteration)
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
        y = encrypt_message("message.txt", n, e)
        # print("p:", p)
        # print("q:", q)
        # print("r:", r)
        # print("e:", e)
        # print("d:", d)
        # print("m:", int.from_bytes(get_message(path="message.txt"), byteorder=sys.byteorder))
        # print("y:", y)
        x_decrypt, time_decrypt = decrypt(y, d, n)
        x_garner, time_garner = garner(y, d, p, q, r)
        print("\ty decrypted with python library:", x_decrypt)
        print("\ty decrypted with Garner:", x_garner)
        print("\tgarner vs python function time:", time_decrypt/time_garner)
        average_time += time_decrypt/time_garner
    print(average_time/10)


if __name__ == '__main__':
    multiprime_RSA()
