import random
import sympy
import numpy as np
from sympy.abc import x


def get_binary():
    is_number = False
    with open("input.txt", "r") as fd:
        content = fd.read()
        if content.isdigit():
            binary = int(content)
            is_number = True
        else:
            binary = ''.join(format(ord(character), "b") for character in content)
            # print(int(binary, 2))
    return binary, is_number


def compute_polinom(x, constants):
    polinom = None
    for constant in constants:
        if polinom is None:
            polinom = constant
        else:
            polinom += constant
        polinom *= x
    return polinom


def getNumber(x, constants):
    polinom = None
    for index in range(len(constants)):
        if polinom is None:
            polinom = constants[index]
        else:
            polinom += constants[index] * x ** index
    return polinom


def compute_reminders(number, prime):
    reminders = []
    # print("input:", number)
    if isinstance(number, str):
        print("binary stuff")
        number = int(number, 2)
    while number:
        reminders.append(number % prime)
        number //= prime
    reminders.reverse()
    return reminders


def encoding(prime, s=1):
    binary, is_number = get_binary()
    if type(binary) is int:
        coef_array = compute_reminders(binary, prime)
    else:
        # print("log2:", int(np.log2(prime)))
        # coef_array = [int(binary[i: i + int(np.log2(prime))], 2) % prime for i in
        #               range(0, len(binary), int(np.log2(prime)))]
        coef_array = [int(binary[i: i + prime - 1], 2) % prime for i in
                      range(0, len(binary), prime - 1)]
        coef_array.reverse()
        # print("after writing in blocks:", coef_array)
    result = [compute_polinom(index, coef_array) % prime for index in range(1, len(coef_array) + 1 + 2 * s + 1)]
    # len(coef_array) = k - 1, so len(coef_array) + 2 * s will be actually equal to n - 1 instead of n
    # range(1,x) also counts up to x - 1, so in the end we should add 2 to len(coef_array) + 2 * s
    print("coefs:", coef_array)
    return result, is_number


def compute_free_coef(z, a, prime, x=0):
    product_of_inverses = []
    inverses = np.zeros(int((prime + 1) / 2))
    free_coef = 0
    check_product = []
    for i in a:
        product_of_inverses = []
        # check_product = []
        for j in a:
            if j != i:
                to_inverse = (i - j) % prime
                if to_inverse >= int((prime + 1) / 2):
                    if inverses[-to_inverse % prime] == 0:
                        # print("compute inverse")
                        inverses[-to_inverse % prime] = sympy.mod_inverse(-to_inverse % prime, prime)
                    product_of_inverses.append(int((x - j) * (-inverses[-to_inverse % prime]) % prime))
                else:
                    if inverses[to_inverse] == 0:
                        # print("compute inverse")
                        inverses[to_inverse] = sympy.mod_inverse(to_inverse, prime)
                    product_of_inverses.append(int((x - j) * inverses[to_inverse] % prime))
                check_product.append((x - j) * sympy.mod_inverse((i - j), prime) % prime)
        # print(inverses)
        # print("check:", check_product)
        # print("product:", product_of_inverses)
        free_coef += z[i - 1] * np.product(product_of_inverses)
        # print(free_coef % prime)
    # print(check_product)
    return free_coef % prime


def polynomial_interpolation(a, z, prime):
    data = [(i, z[i - 1]) for i in a]
    expr = sympy.polys.interpolate(data, x)
    coefs = sympy.Poly(expr, x).coeffs()
    results = []
    for coef in coefs:
        to_prime = str(coef).split("/")
        c = int(to_prime[0]) % prime
        if len(to_prime) == 2:
            c = c * sympy.mod_inverse(int(to_prime[1]), prime) % prime
        results.append(c)
    return results


def polynomial_interpolation(output, a, prime, k):
    matrix = sympy.Matrix([[np.power(x, x_pow) % prime for x_pow in range(k)] for x in a])
    matrix = matrix.inv()
    results = sympy.Matrix([output[x-1] for x in a])
    results.reshape(k, 1)
    matrix = matrix.applyfunc(lambda x: x % prime)
    coefs = matrix * results
    coefs = sympy.matrix2numpy(coefs)
    interpolation = list()
    for coef in coefs:
        if "/" in str(coef):
            division = str(coef).strip("[]").split("/")
            interpolation.append((int(division[0]) % prime) * sympy.mod_inverse(int(division[1]), prime) % prime)
    interpolation.reverse()
    return interpolation


def decoding(output, prime, is_number, s=1):
    n = len(output)
    k = len(output) - 2 * s
    # get samples until free_coeficient is 0
    a = random.sample(range(1, n + 1), k)
    free_coef = compute_free_coef(output, a, prime)
    while free_coef != 0:
        a = random.sample(range(1, n + 1), k)
        free_coef = compute_free_coef(output, a, prime)
    print("a:", a)
    coefs = polynomial_interpolation(output, a, prime, k)
    coefs.pop()
    if is_number:
        print("polynomial interpolation:", coefs)
        coefs.reverse()
        return getNumber(prime, coefs)
    return coefs


prime = 11
output, is_number = encoding(prime)
print("encoding:", output)
# z = [4, 6, 1, 9, 1, 1, 1, 10]
print("decoding:", decoding(output, prime, is_number))
# print("decoding:", decoding(z, prime, is_number))

