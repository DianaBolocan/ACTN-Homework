from Homework3 import solovay_strassen


def compute_s(n, mersenne_number):
    s = 4
    count = 1
    while count != n - 1:
        s = "{0:b}".format(pow(s, 2) - 2)  # % mersenne_number
        x1 = 0
        if len(s) <= n:
            x0 = int(s, 2)
        else:
            x0 = int(s[-n:], 2)
            x1 = int(s[:-n], 2)
        s = x0 + x1
        if s >= mersenne_number:
            s -= mersenne_number
        count += 1
    return s


def run(n=None):
    if not n:
        try:
            n = int(input("N: "))
        except Exception as e:
            print(e)
            return False
    if not solovay_strassen.run(n):
        print("Not Mersenne number")
        return False
    mersenne_number = pow(2, n) - 1
    print("Number:", mersenne_number)
    s = compute_s(n, mersenne_number)
    if s != 0:
        print("Not Mersenne number")
        return False
    print("Mersenne number")
    return True


if __name__ == '__main__':
    run(13)
