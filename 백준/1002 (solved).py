import sys
n = int(sys.stdin.readline())

for _ in range(n):
    x1, y1, r1, x2, y2, r2 = map(int, sys.stdin.readline().split())

    dis = (x2-x1)**2 + (y2-y1)**2

    if x1==x2 and y1==y2 and r1==r2:
        print(-1)
    elif dis > (r1+r2)**2:
        print(0)
    elif dis == (r1+r2)**2:
        print(1)
    elif dis == abs(r1-r2)**2:
        print(1)
    elif dis < abs(r1-r2)**2:
        print(0)
    else:
        print(2)