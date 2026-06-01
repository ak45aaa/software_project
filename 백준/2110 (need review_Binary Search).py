import sys

n, c = map(int, sys.stdin.readline().split())

homes = []
for _ in range(n):
    homes.append(int(sys.stdin.readline()))
    
homes.sort()
    
def can_pose(d):
    count = 1
    last = homes[0]

    for i in range(1, n):
        if homes[i] - last >= d:
            count += 1
            last = homes[i]

    return count >= c
    
left = 1
right = homes[-1] - homes[0]

while left <= right:
    mid = (left + right) // 2

    if can_pose(mid):
        left = mid + 1
    else:
        right = mid - 1

print(right)