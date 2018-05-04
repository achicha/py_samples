"""
input: The first (and the only) input line contains integer number w (1 ≤ w ≤ 100)
output: Print YES, if the boys can divide the watermelon into two parts,
        each of them weighing even number of kilos;
        and NO in the opposite case.
"""


def divide(w):
    if (int(w) / 2) % 2 == 0:
        return 'YES'
    else:
        return 'NO'


if __name__ == "__main__":
    w = input()
    print(divide(w))
