"""
Theatre Square in the capital city of Berland has a rectangular shape with the size n × m meters.
On the occasion of the city's anniversary, a decision was taken to pave the Square with square granite flagstones.
Each flagstone is of the size a × a.
What is the least number of flagstones needed to pave the Square?
It's allowed to cover the surface larger than the Theatre Square, but the Square has to be covered.
It's not allowed to break the flagstones. The sides of flagstones should be parallel to the sides of the Square.

Input
The input contains three positive integer numbers in the first line: n,  m and a (1 ≤  n, m, a ≤ 109).

Output
Write the needed number of flagstones.
"""


def theatre_square(n, m, a):
    x = (n // a + 1) if n % a != 0 else n / a
    y = (m // a + 1) if m % a != 0 else m / a
    return int(x * y)

if __name__ == "__main__":
    n, m, a = input().split(' ')
    print(theatre_square(int(n), int(m), int(a)))



#n,m,a=map(int,input().split())
#print(-n//a*(-m//a))
