import sys

n, k = map(int, sys.stdin.readline().split())

nums = [x for x in range(1, 1001)]
tmp = 2

while True:
    for i in nums:
        if k == 0:
            if i % tmp == 0:
                print(i)
                break
        if i % tmp == 0:
            nums.remove(i)
            k -= 1
    tmp += 1
