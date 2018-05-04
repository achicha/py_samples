"""Input
The first line contains an integer n (1 ≤ n ≤ 100). Each of the following n lines contains one word.
All the words consist of lowercase Latin letters and possess the lengths of from 1 to 100 characters.

Output
Print n lines. The i-th line should contain the result of replacing of the i-th word from the input data.
"""


def long(some_words):
    for word in some_words:
        if len(word) > 10:
            print(word[0] + str(len(word) - 2) + word[-1])
        else:
            print(word)

if __name__ == "__main__":
    number = int(input())
    words = []
    for i in range(number):
        words.append(input())
    long(words)
