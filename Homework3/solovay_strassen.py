import random


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


def run(n=None, k=100):
    if not n:
        try:
            n = int(input("N: "))
        except Exception as e:
            print(e)
            return False
    if n % 2 == 0:
        print("Not prime number")
        return False
    for number in range(k):
        a = random.randint(2, n - 1)
        symbol = jacobi_symbol(a, n)
        if symbol == 0 or pow(a, (n - 1) // 2, n) != symbol % n:
            print("Not prime number")
            return False
    print("Prime number")
    return True


if __name__ == '__main__':
    run(31)
