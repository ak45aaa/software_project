import sys

n = int(sys.stdin.readline())
k = n // 5

best = -1
for i in range(k+1):
    y = n - i*5
    if y % 3 == 0:
        best = i + y//3

print(best)