#### 282A
lst = []
for i in range(int(input())):
    lst.append(input().replace('--','-').replace('++','+').replace('X', ''))
s = '1'.join(lst) + '1'
print(eval(s))

# print(sum('+'in input() or -1 for i in range(int(input()))))
# --------------------------------------------------------------------------------------

#### 96A

s = input()
zero = s.count('0000000')
one = s.count('1111111')
if any((zero, one)):
    print('YES')
else:
    print('NO')

# s=input();print('NYOE S'['0'*7 in s or '1'*7 in s::2])
# --------------------------------------------------------------------------------------


