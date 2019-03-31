import sympy, time, sys


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


def decrypt(y, d, n):
    start = time.time()
    x = pow(y, d, n)
    end = time.time() - start
    return x, end


def generate_pq_primes():
    q = None
    p = sympy.randprime(pow(2, 512), pow(2, 523))
    while q is None:
        q = sympy.randprime(pow(2, 512), pow(2, 523))
        if q == p:
            q = None
    return p, q


def get_quotient(divident, divisor):
    count = 0
    while divident:
        if divident - divisor >= 0:
            count += 1
        divident -= divisor
    return count


def tcr_hensel(y, d, p, q, e):
    start = time.time()
    x = None
    mq = pow(y % q, d % (q - 1), q)
    # mp2 = m1*p + m0
    m0 = pow(y % p, d % (p - 1), p)
    # print(pow(m0, e, p * p))
    # print(get_quotient(y - pow(m0, e, p * p), p))
    # print((y - pow(m0, e, p * p)) // p)
    # print(y == y - pow(m0, e, p*p))
    m1 = (((y - pow(m0, e, p * p)) // p) * sympy.mod_inverse(e * pow(m0, e - 1, p), p)) % p
    mp2 = m1 * p + m0
    x = mp2
    alpha = (((mq - x) % q) * sympy.mod_inverse(mp2, q)) % q
    x += alpha * mp2
    end = time.time() - start
    return x, end


def multipower_RSA(iterations=10):
    average_time = 0
    for iteration in range(iterations):
        print("Iteration:", iteration)
        p, q = generate_pq_primes()
        n = p * p * q
        phi_n = p * (p - 1) * (q - 1)
        e = pow(2, 16) + 1
        d = sympy.mod_inverse(e, phi_n)
        y = encrypt_message("message.txt", n, e)
        # print("p^2:", p ** 2)
        # print("q:", q)
        # print("e:", e)
        # print("d:", d)
        # print("m:", int.from_bytes(get_message(path="message.txt"), byteorder=sys.byteorder))
        # print("y:", y)
        x_tcr, time_tcr = tcr_hensel(y, d, p, q, e)
        x_decrypt, time_decrypt = decrypt(y, d, n)
        print("\tdecrypted with TCR and Hense:", x_tcr)
        print("\tdecrypted with python library:", x_decrypt)
        print("\tTCR and Hensel vs python library:", time_decrypt / time_tcr)
        average_time += time_decrypt / time_tcr
    print(average_time / iteration)


if __name__ == '__main__':
    multipower_RSA()
