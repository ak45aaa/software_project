import sys

t = int(sys.stdin.readline())

def sumf(list1_, list2_):
    return [list1_[0]+list2_[0], list1_[1]+list2_[1]]

list1 = [0, 1]
list0 = [1, 0]

for _ in range(t):
    n = int(sys.stdin.readline())
    temp = 1
    
    lists = [list0, list1]
    
    if n == 0:
        print("1 0")
    elif n == 1:
        print("0 1")
    else:
        while temp < n:
            lists.append(sumf(lists[temp-1], lists[temp]))
            temp += 1
            
        print(lists[-1][0], lists[-1][1])