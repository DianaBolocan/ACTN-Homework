from Homework3 import solovay_strassen


def compute_s(mersen_number, stop=1):
    s = 4
    count = 1
    while count != stop:
        s = (pow(s, 2) - 2) % mersen_number
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
        print("Not Mersen number")
        return False
    mersen_number = pow(2, n) - 1
    print("Number:", mersen_number)
    s = compute_s(mersen_number, n)
    if s != 0:
        print("Not Mersen number")
        return False
    print("Mersen number")
    return True


if __name__ == '__main__':
    run(7)
