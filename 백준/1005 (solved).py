from collections import deque
import sys

# 백준 좆같을때
# 1. input() 대신 sys.stdin.readline() 을 쓰자
# 2. 만약 리스트의 크기를 안다면 .append()말고 인덱스로 접근 해서 값을 바꾸자
# 3. 줄바꿈이 많을 경우 여러개의 print()를 쓰지 말고 문자열 + \n 을 쓰자

test_case_num = int(input())

for k in range(test_case_num):
    n, t_n = map(int, input().split())
    time = list(map(int, input().split()))
    
    graph = [[] for _ in range(n+1)]
    indegree = [0 for _ in range(n+1)]


    for i in range(t_n):
        x, y = map(int, input().split())
        graph[x].append(y)
        indegree[y] += 1
        
    w = int(input())

    dp = [0] * (n+1)
    for i in range(n):
        dp[i+1] = time[i]
        

    queue = deque()
    for i in range(1, n+1):
        if indegree[i] == 0:
            queue.append(i)
    
    while queue:
        cur = queue.popleft()
        for node in graph[cur]:
            dp[node] = max(dp[node], dp[cur]+time[node-1])
            indegree[node] -= 1
            if indegree[node] == 0:
                queue.append(node)
    
    print(dp[w])