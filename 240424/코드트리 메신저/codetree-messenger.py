from sys import stdin
from collections import deque

input = stdin.readline

def setup(commands: list):
    for i in range(1, N + 1):
        parents[i] = commands[i]

    for i in range(1, N + 1):
        authorities[i] = commands[i + N]

        if authorities[i] > 20:
            authorities[i] = 20

    for i in range(1, N + 1):
        cur_node = i
        can_depth = authorities[i]
        tree[cur_node][can_depth] += 1

        while parents[cur_node] and can_depth:
            cur_node = parents[cur_node]
            can_depth -= 1

            if can_depth:
                tree[cur_node][can_depth] += 1
            
            able_counts[cur_node] += 1


def set_alarm(node: int):
    cur_node = parents[node]
    num = 1

    while cur_node:
        for depth in range(num, MAX_DEPTH):
            able_counts[cur_node] += tree[node][depth] if not alarms[node] else -tree[node][depth]

            if depth > num:
                tree[cur_node][depth - num] += tree[node][depth] if not alarms[node] else -tree[node][depth]
            
        if not alarms[cur_node]:
            break
        
        cur_node = parents[cur_node]
        num += 1
    
    alarms[node] = not alarms[node]

def set_power(node: int, power: int):
    before_power = authorities[node]
    power = min(power, 20)

    authorities[node] = power

    tree[node][before_power] -= 1
    if alarms[node]:
        cur_node = parents[node]
        num = 1

        while cur_node:
            if before_power >= num:
                able_counts[cur_node] -= 1
            if before_power > num:
                tree[cur_node][before_power - num] -= 1
            if not alarms[cur_node]:
                break
            
            cur_node = parents[cur_node]
            num += 1

    tree[node][power] += 1
    if alarms[node]:
        cur_node = parents[node]
        num = 1

        while cur_node:
            if power >= num:
                able_counts[cur_node] += 1
            if power > num:
                tree[cur_node][power - num] += 1
            if not alarms[cur_node]:
                break

            cur_node = parents[cur_node]
            num += 1

def exchange_node(a: int, b: int):
    before_alarm_a = alarms[a]
    before_alarm_b = alarms[b]

    if before_alarm_a:
        set_alarm(a)
    if before_alarm_b:
        set_alarm(b)

    parents[a], parents[b] = parents[b], parents[a]

    if before_alarm_a:
        set_alarm(a)
    if before_alarm_b:
        set_alarm(b) 


def can_alarms(node: int)-> int:
    return able_counts[node]


if __name__ == '__main__':
    MAX_NODE = 100001
    MAX_DEPTH = 21

    parents = [0] * MAX_NODE
    authorities = [0] * MAX_NODE
    able_counts = [0] * MAX_NODE
    alarms = [True] * MAX_NODE
    tree = [[0 for _ in range(MAX_DEPTH)] for _ in range(MAX_NODE)]

    N, Q = map(int, input().split())

    for q in range(Q):
        commands = list(map(int, input().split()))

        command = commands[0]

        if command == 100:
            setup(commands)
        elif command == 200:
            set_alarm(commands[1])
        elif command == 300:
            set_power(commands[1], commands[2])
        elif command == 400:
            exchange_node(commands[1], commands[2])
        elif command == 500:
            print(can_alarms(commands[1]))