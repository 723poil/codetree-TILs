from sys import stdin

input = stdin.readline

dd = [(-1, 0), (0, 1), (1, 0), (0, -1)]
# L - 체스판 크기, N - 기사 수, Q - 왕의 명령
L, N, Q = map(int, input().split())

chess = [[-1 for _ in range(L+1)]]
knights = dict()
knights_map = [[0 for _ in range(L+1)] for _ in range(L+1)]

# 초기 기사들의 위치 지정
def set_knight(left_up: tuple, right_down: tuple, knight: int):
    global knights_map

    for y in range(left_up[0], right_down[0]+1):
        for x in range(left_up[1], right_down[1]+1):
            knights_map[y][x] = knight

# 움직이려는 위치에 벽, 기사들이 있는지 확인
def check_map(left_up: tuple, right_down: tuple, dir: int):
    global dd, L, chess, knights_map, knights
    
    check_range = ()
    result = []
    sy, ey, sx, ex = (0, 0, 0, 0)

    if dir == 0:
        check_range = (left_up[0] + dd[dir][0], right_down[1])
        sy, sx, ey, ex = (check_range[0], left_up[1], check_range[0]+1, right_down[1]+1)
    elif dir == 2:
        check_range = (right_down[0] + dd[dir][0], right_down[1])
        sy, sx, ey, ex = (check_range[0], left_up[1], check_range[0]+1, right_down[1]+1)
    elif dir == 1:
        check_range = (left_up[0], right_down[1] + dd[dir][1])
        sy, sx, ey, ex = (left_up[0], check_range[1], right_down[0]+1, check_range[1]+1)
    else:
        check_range = (left_up[0], left_up[1] + dd[dir][1])
        sy, sx, ey, ex = (left_up[0], check_range[1], right_down[0]+1, check_range[1]+1)
    
    for dy in range(sy, ey):
        for dx in range(sx, ex):
            if not (0 < dy <= L and 0 < dx <= L) or chess[dy][dx] == 2:
                return [(2, 0)]
            
            if knights_map[dy][dx] != 0:
                result.append((3, knights_map[dy][dx]))
    
    if len(result) == 0:
        return result

    result = list(set(result))

    rr = []
    i = 0
    while i < len(result):
        knight = result[i][1]
        klu = knights[knight][0]
        krd = knights[knight][1]

        rrr = check_map(klu, krd, dir)

        if len(rrr) != 0 and rrr[0][0] == 2:
            return [(2, 0)]

        rr += rrr
        
        i+= 1

    result += rr

    return result

# 직접 움직이거나 밀려나는 기사들의 위치 재지정
def move_knight(isAttacked: bool, knight: int, dir: int):
    global dd, L, chess, knights_map, knights

    left_up = knights[knight][0]
    right_down = knights[knight][1]
    k = knights[knight][2]

    dmg = 0

    for dy in range(left_up[0], right_down[0]+1):
        for dx in range(left_up[1], right_down[1]+1):
            if knights_map[dy][dx] == knight:
                knights_map[dy][dx] = 0

    for dy in range(left_up[0], right_down[0]+1):
        for dx in range(left_up[1], right_down[1]+1):
            knights_map[dy+dd[dir][0]][dx+dd[dir][1]] = knight

            if chess[dy+dd[dir][0]][dx+dd[dir][1]] == 1:
                dmg += 1

    if isAttacked and dmg >= k:
        for dy in range(left_up[0], right_down[0]+1):
            for dx in range(left_up[1], right_down[1]+1): 
                knights_map[dy+dd[dir][0]][dx+dd[dir][1]] = 0
        del knights[knight]
        return
    elif isAttacked:
        knights[knight][2] -= dmg
        knights[knight][3] += dmg

    knights[knight][0] = (left_up[0] + dd[dir][0], left_up[1] + dd[dir][1])
    knights[knight][1] = (right_down[0] + dd[dir][0], right_down[1] + dd[dir][1])

# 왕의 명령 수행
def command_knight(knight: int, dir: int):
    global dd, chess, knights_map, knights
        
    left_up = knights[knight][0]
    right_down = knights[knight][1]

    command = check_map(left_up, right_down, dir)

    if len(command) != 0 and command[0][0] == 2:
        return

    move_knight(False, knight, dir)
    
    for cc in command:
        kk = cc[1]
        move_knight(True, kk, dir)

def solution():    
    global L, N, Q, chess, knights_map, knights

    for _ in range(L):
        cs = list(map(int, input().split()))

        chess.append([-1] + cs)

    for i in range(1, N+1):
        r, c, h, w, k = map(int, input().split())

        left_up = (r, c)
        right_down = (r+h-1, c+w-1)
        knights[i] = [left_up, right_down, k, 0]

        # 기사들 위치 지정
        set_knight(left_up, right_down, i)

    for _ in range(Q):
        ks, q = map(int, input().split())

        if not knights.get(ks):
            continue

        command_knight(ks, q)
    
    count = 0
    for key in knights.keys():
        count += knights[key][3]

    return count

print(solution())