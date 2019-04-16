import random
import sympy
from Homework2 import multiprimeRSA as algorithm


def jacobi_symbol(a, n):
    if (n < 0) or (n % 2 == 0):
        return 0
    j = 1
    if a < 0:
        a = -a
        if n % 4 == 3:
            j = -j
    while a != 0:
        while a % 2 == 0:
            # procesam multiplii de 2
            a //= 2
            if (n % 8 == 3) or (n % 8 == 5):
                j = -j

        # Legea reciprocitatii
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            j = -j
        a %= n
    if n == 1:
        return j
    else:
        return 0


def run(n=None):
    if not n:
        try:
            n = int(input("N: "))
        except Exception as e:
            print(e)
            return False
    a = random.randint(2, n - 2)
    print("a:", a)
    if algorithm.gcd(n, a) != 1:
        print("(1): n compus")
        return False
    rest = pow(a, (n - 1) * sympy.mod_inverse(2, n), n)
    print("r:", rest)
    if rest not in [1, n - 1]:
        print("(2): n compus")
        return False
    symbol = jacobi_symbol(a, n)
    print("Jacoby symbol:", symbol)
    print("rest:",rest)
    if symbol != rest:
        print("(3): n compus")
        return False
    print("n prim")
    return True


if __name__ == '__main__':
    run()
