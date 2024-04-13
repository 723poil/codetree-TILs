from collections import deque

x = [1, 0, -1, 0]
y = [0, 1, 0, -1]

xx = [-1, 0, 1, -1, 1, -1, 0, 1]
yy = [-1, -1, -1, 0, 0, 1, 1, 1]

N, M, K = map(int, input().split())

class Turret:
    def __init__(self, n, m, t, p):
        self.m = m
        self.n = n
        self.p = p
        self.t = t

board = [list(map(int, input().split())) for _ in range(N)]
time = [[0 for _ in range(M)] for _ in range(N)]

visited = [[0 for _ in range(M)] for _ in range(N)]
before_route_n = [[0 for _ in range(M)] for _ in range(N)]
before_route_m = [[0 for _ in range(M)] for _ in range(N)]

isRelAttack = [[False for _ in range(M)] for _ in range(N)]

alive_turrets = []

def check():
    for n in range(N):
        for m in range(M):
            visited[n][m] = False
            isRelAttack[n][m] = False

def find_attacker(k: int) -> Turret:
    alive_turrets.sort(key= lambda x: (x.p, -x.t, -(x.m + x.n), -x.m))

    board[alive_turrets[0].n][alive_turrets[0].m] += N + M
    time[alive_turrets[0].n][alive_turrets[0].m] = k
    alive_turrets[0].p += (N + M)
    alive_turrets[0].t = k
    isRelAttack[alive_turrets[0].n][alive_turrets[0].m] = True

    return alive_turrets[0]

def start_attack(attaker: Turret, target: Turret):

    q = deque()
    visited[attaker.n][attaker.m] = True
    q.append((attaker.n, attaker.m))

    canLazer = False

    while q:
        nn, mm = q.popleft()

        if nn == target.n and mm == target.m:
            canLazer = True
            break

        for i in range(4):
            next_n = (nn + y[i]) % N
            next_m = (mm + x[i]) % M

            if visited[next_n][next_m]:
                continue
            
            if board[next_n][next_m] == 0:
                continue

            visited[next_n][next_m] = True
            before_route_n[next_n][next_m] = nn
            before_route_m[next_n][next_m] = mm
            q.append((next_n, next_m))

    if not canLazer:
        other_attack(attaker, target)
        return

    board[target.n][target.m] = 0 if board[target.n][target.m] < attaker.p else board[target.n][target.m] - attaker.p
    isRelAttack[target.n][target.m] = True

    bn = before_route_n[target.n][target.m]
    bm = before_route_m[target.n][target.m]    

    while not (bn == attaker.n and bm == attaker.m):
        board[bn][bm] = 0 if board[bn][bm] < (attaker.p // 2) else board[bn][bm] - attaker.p // 2
        isRelAttack[bn][bm] = True

        temp_n = before_route_n[bn][bm]
        temp_m = before_route_m[bn][bm]

        bn = temp_n
        bm = temp_m

    
def other_attack(attaker: Turret, target: Turret):

    board[target.n][target.m] = 0 if board[target.n][target.m] < attaker.p else board[target.n][target.m] - attaker.p
    isRelAttack[target.n][target.m] = True

    for i in range(8):
        next_n = (target.n + yy[i]) % N
        next_m = (target.m + xx[i]) % M

        if next_n == attaker.n and next_m == attaker.m:
            continue

        board[next_n][next_m] = 0 if board[next_n][next_m] < (attaker.p // 2) else board[next_n][next_m] - (attaker.p // 2)
        isRelAttack[next_n][next_m] = True


def check_not_rel_attack():
    for n in range(N):
        for m in range(M):
            if board[n][m] != 0 and not isRelAttack[n][m]:
                board[n][m] += 1

for k in range(1, K+1):

    alive_turrets = []
    for n in range(N):
        for m in range(M):
            if board[n][m] > 0:
                turret = Turret(n, m, time[n][m], board[n][m])
                alive_turrets.append(turret)

    if len(alive_turrets) <= 1:
        break

    check()

    attacker = find_attacker(k)
    
    start_attack(attacker, alive_turrets[-1])

    check_not_rel_attack()

result = 0
for n in range(N):
    for m in range(M):
        result = max(result, board[n][m])

print(result)