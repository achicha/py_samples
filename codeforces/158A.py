"""
Input
The first line of the input contains two integers n and k (1 ≤ k ≤ n ≤ 50) separated by a single space.

The second line contains n space-separated integers a1, a2, ..., an (0 ≤ ai ≤ 100),
where ai is the score earned by the participant who got the i-th place.
The given sequence is non-increasing (that is, for all i from 1 to n - 1 the following condition is fulfilled: ai ≥ ai + 1).

Output
Output the number of participants who advance to the next round.
"""


def next_round(n, k, a_lst):
    """
    8 5
    10 9 8 7 7 7 5 5
    """
    wnrs = sorted([int(i) for i in a_lst if int(i) > 0], reverse=True)
    # if no winners
    if not len(wnrs):
        return 0

    # if all of them are winners
    if len(wnrs) <= k:
        return len(wnrs)

    # if someone has the same result, keep him in the winners and exclude others.
    current_k = k - 1
    next_k = 0
    while True:
        next_k += 1
        if current_k + next_k <= len(wnrs) - 1 and wnrs[current_k] == wnrs[current_k + next_k]:
            continue
        else:
            return len(wnrs[:k + next_k - 1])

if __name__ == "__main__":
    n, k = input().split(' ')
    a_lst = input().split(' ')
    winners = next_round(int(n), int(k), a_lst)
    print(winners)
