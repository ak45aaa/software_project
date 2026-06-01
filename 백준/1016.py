import sys

# 에라토스테네스의 체 를 알아야하고
# ??왜
# 골드1을 너무 얕보았다
# 이거나아ㅣ먼ㄹ;어

mini, maxi = map(int, sys.stdin.readline().split())

cnt = 0
for num in range(mini, maxi+1):
    if num == 1 or num == 2 or num == 3:
        continue
    else:
        flag = False
        for i in range(2, num//2+1):
            if num % i**2 == 0:
                flag = True
                break
        if flag:
            cnt += 1

print(maxi-mini+1-cnt)