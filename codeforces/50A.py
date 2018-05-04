"""
1. Each domino completely covers two squares.

2. No two dominoes overlap.

3. Each domino lies entirely inside the board. It is allowed to touch the edges of the board.

Find the maximum number of dominoes, which can be placed under these restrictions.

Input
In a single line you are given two integers M and N — board sizes in squares (1 ≤ M ≤ N ≤ 16).

Output
Output one number — the maximal number of dominoes, which can be placed.

"""
dim = [int(i) for i in input().split(' ')]
board = dim[0] * dim[1]
ans = board // 2
print(ans)


# print(eval('*'.join(input().split()))//2)