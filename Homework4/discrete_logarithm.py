import random
import math
import sympy
from Homework4 import primitive_root_modulo


def shanks(beta, alpha, p):
    m = math.ceil(math.sqrt(p - 1))
    lista = list()
    for j in range(m):
        lista.append(pow(alpha, j, p))
    lista.sort()
    print(lista)
    for i in range(m):
        value = beta * (sympy.mod_inverse(alpha, p) ** (m * i)) % p
        print("Searching for:", value)
        if value in lista:
            break
    j = -1
    for index in range(len(lista)):
        if value == lista[index]:
            j = index
            break
    print("i: {}, j: {}, m: {}".format(i, j, m))
    return (i * m + j) % p if j != -1 else "Couldn't find the result"


if __name__ == '__main__':
    primitve_root, prime = primitive_root_modulo.generate(limit=10)
    number = random.randint(1, prime - 1)
    print("Shanks for alpha {}, beta {} and prime {}".format(number, primitve_root, prime))
    print(shanks(number, primitve_root, prime))
    print("Shanks for alpha {}, beta {} and prime {}".format(11, 2, 13))
    print(shanks(11, 2, 13))
