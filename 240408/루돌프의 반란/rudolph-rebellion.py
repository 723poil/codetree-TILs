from sys import stdin

input = stdin.readline

# 두 칸 사이의 거리 계산
def distance(one: list, two: list) -> int:
    return (abs(one[0] - two[0]) ** 2) + (abs(one[1] - two[1]) ** 2)

# 산타 살아있으면 점수 추가 및 다 탈락했을 경우 False 반환
def alive_santa_one_point(P: int, alive_santas: list, santas: list) -> bool:
    count = 0

    for p in range(1, P+1):
        if alive_santas[p]:
            santas[p][1] += 1
            count += 1
    
    if count == 0:
        return False
    return True

def find_closest_santa(rudol: list, santas: list, alive_santas: list) -> int:
    dis_list = []

    for p in range(1, P+1):
        if not alive_santas[p]:
            continue
        
        dis = distance(rudol, santas[p][2])
        dis_list.append([p, dis, santas[p][2]])

    dis_list.sort(key= lambda x: (x[1], -x[2][0], -x[2][1]))

    return dis_list[0][0]

def find_rudol_dir(rudol: list, santa: list) -> list:
    diff_r = santa[0] - rudol[0]
    diff_c = santa[1] - rudol[1]

    if diff_r == 0:
        return [0, (diff_c // abs(diff_c))]

    if diff_c == 0:
        return [(diff_r // abs(diff_r)), 0]
    
    return [(diff_r // abs(diff_r)), (diff_c // abs(diff_c))]

# 루돌프 움직이기
def move_rudol(rudol: list, santas: list, alive_santas: list, boards: list, K: int, C: int, N: int):
    boards[rudol[0]][rudol[1]] = -1

    # 루돌프는 가장 가까운 산타를 향해 1칸 돌진합니다.
    # 만약 가장 가까운 산타가 2명 이상이라면, r 좌표가 큰 산타를 향해 돌진합니다.
    # r이 동일한 경우, c 좌표가 큰 산타를 향해 돌진합니다.
    # 루돌프는 기절한 산타를 돌진 대상으로 선택할 수 있습니다.
    cloest_santa = find_closest_santa(rudol, santas, alive_santas)

    # 루돌프는 8방향 중 하나로 돌진할 수 있습니다.
    # 가장 우선순위가 높은 산타를 향해 8방향 중 가장 가까워지는 방향
    opt_dir = find_rudol_dir(rudol, santas[cloest_santa][2])

    rudol[0] += opt_dir[0]
    rudol[1] += opt_dir[1]

    # 이동한 지점에 산타가 있는지 확인
    if boards[rudol[0]][rudol[1]] != -1:
        # 루돌프가 움직여서 충돌이 일어난 경우, 해당 산타는 C만큼의 점수를 얻게 됩니다.
        santas[boards[rudol[0]][rudol[1]]][1] += C
        # 산타는 루돌프와의 충돌 후 기절을 하게 됩니다.
        santas[boards[rudol[0]][rudol[1]]][3] = K+1
        
        # 산타 밀려나는거 계산
        # 루돌프 -> 산타  루돌프가 이동해온 방향으로 C 칸 만큼 밀려나게 됩니다.
        conflict(cloest_santa, C, opt_dir, alive_santas, santas, boards, K, N)

    boards[rudol[0]][rudol[1]] = 0


def find_santa_dir(rudol: list, santa: list, boards: list, p: int) -> list:
    # 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동
    diff_r = rudol[0] - santa[0]
    diff_c = rudol[1] - santa[1]

    diff_r = diff_r // abs(diff_r) if diff_r != 0 else 0
    diff_c = diff_c // abs(diff_c) if diff_c != 0 else 0

    r = [-1, 0, 1, 0]
    c = [0, 1, 0, -1]

    fl = []

    for i in range(4):
        expected_santa = [santa[0] + r[i], santa[1] + c[i]]
        if diff_r != 0 and r[i] == diff_r and boards[expected_santa[0]][expected_santa[1]] <= 0:
             fl.append([r[i], c[i], distance(rudol, expected_santa)])
        if diff_c != 0 and c[i] == diff_c and boards[expected_santa[0]][expected_santa[1]] <= 0:
            fl.append([r[i], c[i], distance(rudol, expected_santa)])

    if len(fl) == 0:
        return [0, 0]

    fl.sort(key= lambda x: (x[2], r.index(x[0]) + c.index(x[1])))

    return [fl[0][0], fl[0][1]]

    # 산타는 다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.
    # 움직일 수 있는 칸이 있더라도 만약 루돌프로부터 가까워질 수 있는 방법이 없다면 산타는 움직이지 않습니다.
    # 산타는 상하좌우로 인접한 4방향 중 한 곳으로 움직일 수 있습니다. 이때 가장 가까워질 수 있는 방향이 여러 개라면, 상우하좌 우선순위에 맞춰 움직입니다.

def move_santa(rudol: list, santa: int, santas: list, alive_santas: list, boards: list, K: int, D: int, N: int):
    
    opt_dir = find_santa_dir(rudol, santas[santa][2], boards, santa)

    if opt_dir[0] == 0 and opt_dir[1] == 0:
        return

    boards[santas[santa][2][0]][santas[santa][2][1]] = -1

    santas[santa][2] = [santas[santa][2][0] + opt_dir[0], santas[santa][2][1] + opt_dir[1]]
    santa_cur = santas[santa][2]

    # 산타 -> 루돌프 해당 산타는 D만큼의 점수를 얻게 됩니다. 이와 동시에 산타는 자신이 이동해온 반대 방향으로 D 칸 만큼 밀려나게 됩니다.
    if boards[santa_cur[0]][santa_cur[1]] == 0:
        santas[santa][1] += D
        santas[santa][3] = K+1
        conflict(santa, D, [-opt_dir[0], -opt_dir[1]], alive_santas, santas, boards, K, N)
    else:
        boards[santas[santa][2][0]][santas[santa][2][1]] = santa

# 산타와 루돌프가 같은 칸에 있게 되면 충돌이 발생
def conflict(santa: int, dis: int, dir: list, alive_santas: list, santas: list, boards: list, K: int, N: int):
    real_dis = [dir[0] * dis, dir[1] * dis]

    # 밀려나는 것은 포물선 모양을 그리며 밀려나는 것이기 때문에 이동하는 도중에 충돌이 일어나지는 않고 정확히 원하는 위치에 도달하게 됩니다.
    if not (0 < santas[santa][2][0] + real_dis[0] <= N and 0 < santas[santa][2][1] + real_dis[1] <= N):
        alive_santas[santa] = False
        boards[santas[santa][2][0]][santas[santa][2][1]] = -1
        return

    santas[santa][2] = [santas[santa][2][0] + real_dis[0], santas[santa][2][1] + real_dis[1]]
    
    # 만약 밀려난 칸에 다른 산타가 있는 경우 상호작용이 발생
    # 산타는 충돌 후 착지하게 되는 칸에 다른 산타가 있다면 그 산타는 1칸 해당 방향으로 밀려나게 됩니다.
    # 그 옆에 산타가 있다면 연쇄적으로 1칸씩 밀려나는 것을 반복하게 됩니다.
    another_santa = boards[santas[santa][2][0]][santas[santa][2][1]]
    if another_santa != -1:
        # 현재가 k번째 턴이었다면, (k+1)번째 턴까지 기절하게 되어 (k+2)번째 턴부터 다시 정상상태가 됩니다.
        # 기절한 도중 충돌이나 상호작용으로 인해 밀려날 수는 있습니다.
        conflict(another_santa, 1, dir, alive_santas, santas, boards, K, N)

    boards[santas[santa][2][0]][santas[santa][2][1]] = santa

if __name__ == "__main__":
    # N - 게임판 크기, M - 턴 수, P - 산타 수, C - 루돌푸가 움직였을때 점수, D - 산타가 움직였을때 점수
    N, M, P, C, D = map(int, input().split())

    # 게임판은 N×N 크기의 격자로 이루어져 있습니다. 
    # 각 위치는 (r,c), 좌상단은 (1,1)
    boards = [[-1 for _ in range(N+2)] for _ in range(N+2)]

    # 루돌프 시작 좌표
    rudol = list(map(int, input().split()))
    boards[rudol[0]][rudol[1]] = 0

    # 1번부터 P번까지 P 명의 산타들
    santas = [list()] * (P+1)
    alive_santas = [True] * (P+1)

    for i in range(P):
        santa = list(map(int, input().split()))
        boards[santa[1]][santa[2]] = santa[0]

        # 산타번호, 산타 점수, 산타 위치, 
        santas[santa[0]] = [santa[0], 0, [santa[1], santa[2]], -1]

    # 게임은 총 M 개의 턴에 걸쳐 진행되며 매 턴마다 루돌프와 산타들이 한 번씩 움직입니다.
    for k in range(1, M+1):

        # 루돌프 움직이기
        move_rudol(rudol, santas, alive_santas, boards, k, C, N)

        # 산타 움직이기
        for p in range(1, P+1):
            # 밖에 있는 산타들
            if not alive_santas[p]:
                continue
            
            # 기절
            if santas[p][3] != -1 and santas[p][3] >= k:
                continue

            # 산타 움직이기
            move_santa(rudol, p, santas, alive_santas, boards, k, D, N)

        # 매 턴 이후 아직 탈락하지 않은 산타들에게는 1점씩을 추가로 부여합니다.
        alive = alive_santa_one_point(P, alive_santas, santas)

        # 만약 P 명의 산타가 모두 게임에서 탈락하게 된다면 그 즉시 게임이 종료됩니다.
        if not alive:
            break

        

    # 각 산타가 얻은 최종 점수 출력
    for santa in santas[1:]:
        print(santa[1], end=" ")