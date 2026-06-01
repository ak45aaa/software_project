import sys

n = int(sys.stdin.readline())
stack = []

for _ in range(n):
    order = sys.stdin.readline().strip()
    
    if order[:4] == "push":
        _, x = order.split()
        stack.append(int(x))
    elif order == "pop":
        if stack:
            print(stack.pop(len(stack)-1))
        else:
            print(-1)
    elif order == "size":
        print(len(stack))
    elif order == "empty":
        if stack:
            print(0)
        else:
            print(1)
    else:
        if stack:
            print(stack[len(stack)-1])
        else:
            print(-1)
    