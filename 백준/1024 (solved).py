import sys

n, l = map(int, sys.stdin.readline().split())
done = False

for i in range(l, 101):
    if i%2 == 0:
        if n/i - int(n/i) == 0.5:
            if int(n/i)+1 >= i/2:
                for temp in range(i):
                    print(int(int(n/i)-i/2+1+temp), end=" ")
                done = True
                break
    else:
        if n/i - int(n/i) == 0:
            if n/i >= (i-1)/2:
                for temp in range(i):
                    print(int(n/i-(i-1)/2+temp), end=" ")
                done = True
                break

if not done:
    print(-1)