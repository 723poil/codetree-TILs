from sys import stdin

input = stdin.readline

def can_alarms(node: int, depth: int = 1)-> int:
    count = 0

    # 1. 자식노드 부터 시작(depth + 1)
    # 2. setup설정이 꺼져있으면 넘기기
    # 3. 세기를 확인하고 가능하면 + 1
    for i, p in enumerate(tree):
        if p == node and alarms[i] and authorities[i] >= depth:
            count += 1
            count += can_alarms(i+1, depth + 1)

    return count


if __name__ == '__main__':
    N, Q = map(int, input().split())

    tree = []
    authorities = []
    alarms = [True for _ in range(N)]

    for q in range(Q):
        commands = list(map(int, input().split()))

        command = commands[0]

        if command == 100:
            tree = commands[1:N+1]
            authorities = commands[N+1:]
        
        elif command == 200:
            alarms[commands[1]-1] = not alarms[commands[1]-1]
        
        elif command == 300:
            authorities[commands[1]-1] = commands[2]
        
        elif command == 400:
            a = commands[1]
            b = commands[2]

            temp = tree[a-1]
            tree[a-1] = tree[b-1]
            tree[b-1] = temp

        elif command == 500:
            print(can_alarms(commands[1]))