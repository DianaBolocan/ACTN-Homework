from Homework3 import solovay_strassen


def compute_s(stop=1):
    s = 4
    count = 1

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


if __name__ == '__main__':
    run()
