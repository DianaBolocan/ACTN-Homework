import random
from sympy import mod_inverse


def get_binary():
    with open("input.txt", "r") as fd:
        content = fd.read()
        if content.isdigit():
            binary = int(content)
        else:
            binary = ''.join(format(ord(character), "b") for character in content)
    return binary


def compute_polinom(x, constants):
    polinom = None
    for constant in constants:
        if polinom is None:
            polinom = constant
        else:
            polinom += constant
        polinom *= x
    return polinom


def compute_reminders(number, prime):
    reminders = []
    while number:
        reminders.append(number % prime)
        number //= prime
    reminders.reverse()
    return reminders


def encoding(prime, s=1):
    binary = get_binary()
    if type(binary) is int:
        coef_array = compute_reminders(binary, prime)
    else:
        coef_array = [int(binary[i: i + prime - 1], 2) % prime for i in range(0, len(binary), prime - 1)]
        coef_array.reverse()
    result = [compute_polinom(index, coef_array) % prime for index in range(1, len(coef_array) + 1 + 2 * s + 1)]
    # len(coef_array) = k - 1, so len(coef_array) + 2 * s will be actually equal to n - 1 instead of n
    # range(1,x) also counts up to x - 1, so in the end we should add 2 to len(coef_array) + 2 * s
    print(coef_array)
    return result


def compute_product_of_inverse(a, prime, x=0):
    product_of_inverses = []
    for i in a:
        for j in a:
            product_of_inverses.append((x - j) * mod_inverse((i - j), prime))
    return product_of_inverses


def decoding(output, prime, s=1):
    result = None
    # get samples until free_coeficient is 0
    a = random.sample(output, len(output) - 2 * s)
    print(a)
    # inverses = compute_product_of_inverse(a, prime)
    # print(inverses)
    free_coeficient = None
    return result


prime = 11
print(encoding(prime))
z = [9, 2, 6, 5, 8]
decoding(z, prime)
