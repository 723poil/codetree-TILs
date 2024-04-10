from sys import stdin

input = stdin.readline

r = [-1, 1, 0 ,0]
c = [0, 0, -1, 1]

# 두 위치 (x1,y1), (x2,y2)의 최단거리는 ∣x1−x2∣+∣y1−y2∣로 정의됩니다.
# def optimal_distance(one: list, two: list) -> int:

#     return abs(one[0] - two[0]) + abs(one[1] - two[1])

# 이동방향 잡기
def find_runner_dir(exit: list, runner: list, miro: list) -> int:

    # 상하좌우로 움직일 수 있으며, 벽이 없는 곳으로 이동할 수 있습니다.
    # 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
    # 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시합니다.
    # 참가가가 움직일 수 없는 상황이라면, 움직이지 않습니다.
    
    diff_r = exit[0] - runner[0]
    diff_c = exit[1] - runner[1]

    all_not_zero = diff_c != 0 and diff_r != 0

    if diff_c == 0 and miro[runner[0] + (diff_r // abs(diff_r))][runner[1]] == 0:
        return 0 if diff_r < 0 else 1
    
    if diff_r == 0 and miro[runner[0]][runner[1]  + (diff_c // abs(diff_c))] == 0:
        return 2 if diff_c < 0 else 3
    
    if all_not_zero and miro[runner[0] + (diff_r // abs(diff_r))][runner[1]] == 0:
        return 0 if diff_r < 0 else 1
    
    if all_not_zero and miro[runner[0]][runner[1] + (diff_c // abs(diff_c))] == 0:
        return 2 if diff_c < 0 else 3

    return -1


# 참가자들 움직이기
def move_runner(exit: list, miro: list, runner: list, arrive: list, m: int, dis: int) -> int:
    
    optimal_dir = find_runner_dir(exit, runner, miro)

    if optimal_dir == -1:
        return dis

    runner[0] += r[optimal_dir]
    runner[1] += c[optimal_dir]

    if tuple(exit) == tuple(runner):
        arrive[m] = True

    dis += 1
    return dis

# 정사각형 오른쪽 끝의 좌표 및 길이 반환
def find_square(exit: list, runners: list, arrive: list) -> list:

    squares = []

    # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡습니다.
    # 가장 작은 크기를 갖는 정사각형이 2개 이상이라면, 좌상단 r 좌표가 작은 것이 우선되고, 그래도 같으면 c 좌표가 작은 것이 우선됩니다.
    for m in range(len(runners)):
        if arrive[m]:
            continue

        dis_sq = max(abs(exit[0] - runners[m][0]), abs(exit[1] - runners[m][1])) + 1

        # 두 좌표중 큰쪽을 구한 후 미로 안에 넣을 수 있는 정사각형인지 확인
        max_cur = [max(exit[0], runners[m][0]), max(exit[1], runners[m][1])]

        # r, c 둘다 작을때
        if max_cur[0] < dis_sq and max_cur[1] < dis_sq:
            squares.append([dis_sq, dis_sq, dis_sq])
            continue

        # r 이 작을 때
        if max_cur[0] < dis_sq:
            squares.append([dis_sq, max_cur[1], dis_sq])
            continue

        # c 가 작을 때
        if max_cur[1] < dis_sq:
            squares.append([max_cur[0], dis_sq, dis_sq])
            continue

        squares.append([max_cur[0], max_cur[1], dis_sq])

    squares.sort(key= lambda x: (x[2], x[0], x[1]))

    return squares[0]


def rotate_real(miro: list, square: list, exit: list, runners: list):

    temp_miro = [[0 for _ in range(square[2]+1)] for _ in range(square[2]+1)]
 
    diff_r = square[0] - square[2]
    diff_c = square[1] - square[2]

    for rr in range(1, square[2]+1):
        for cc in range(1, square[2]+1):
            temp_miro[cc][square[2] - rr + 1] = miro[rr + diff_r][cc + diff_c]

    for rr in range(1, square[2]+1):
        for cc in range(1, square[2]+1):
            miro[rr + diff_r][cc + diff_c] = temp_miro[rr][cc] 
    
    for m in range(len(runners)):
        if diff_r < runners[m][0] <= square[0] and diff_c < runners[m][1] <= square[1]:
            tmr = runners[m][0] - diff_r
            tmc = runners[m][1] - diff_c

            runners[m][0] = tmc + diff_r
            runners[m][1] = square[2] - (tmr) + 1 + diff_c

    tmr = exit[0] - diff_r
    tmc = exit[1] - diff_c

    exit[0] = tmc + diff_r
    exit[1] = square[2] - (tmr) + 1 + diff_c

# 미로 회전
def rotate_miro(exit: list, miro: list, runners: list, arrive: list):

    square = find_square(exit, runners, arrive)

    # 회전된 벽은 내구도가 1씩 깎입니다.
    for rr in range(square[0]-square[2]+1, square[0]+1):
        for cc in range(square[1]-square[2]+1, square[1]+1):
            if miro[rr][cc] > 0:
                miro[rr][cc] -= 1

    # 선택된 정사각형은 시계방향으로 90도 회전
    rotate_real(miro, square, exit, runners)

if __name__ == '__main__':

    # 미로의 크기, 참가자 수, 게임 시간
    N, M, K = map(int, input().split())

    # 미로는 N×N 크기의 격자
    miro = [list()]
    runners = []
    arrive = [False] * M
    dis = 0

    for _ in range(N):
        # 빈칸
        # - 참가자가 이동 가능한 칸입니다.

        # 벽
        # - 참가자가 이동할 수 없는 칸입니다.
        # - 1이상 9이하의 내구도를 갖고 있습니다.
        # - 회전할 때, 내구도가 1씩 깎입니다.
        # - 내구도가 0이 되면, 빈 칸으로 변경됩니다.
        miro.append([0] + list(map(int, input().split())))

    for _ in range(M):
        runners.append(list(map(int, input().split())))

    # 출구
    # - 참가자가 해당 칸에 도달하면, 즉시 탈출합니다.
    exit = list(map(int, input().split()))


    for k in range(1, K+1):

        for m in range(M):
            if arrive[m]:
                continue

            # 1초마다 모든 참가자는 한 칸씩 움직입니다.
            # 모든 참가자는 동시에 움직입니다.
            # 한 칸에 2명 이상의 참가자가 있을 수 있습니다.
            dis = move_runner(exit, miro, runners[m], arrive, m, dis)

        # K초 동안 위의 과정을 계속 반복됩니다. 만약 K초 전에 모든 참가자가 탈출에 성공한다면, 게임이 끝납니다.
        if False not in arrive:
            break
            
        # 모든 참가자가 이동을 끝냈으면, 다음 조건에 의해 미로가 회전합니다.
        rotate_miro(exit, miro, runners, arrive)

    # 모든 참가자들의 이동 거리 합과 출구 좌표를 출력하는 프로그램을 작성해보세요.
    print(dis)
    print(exit[0], exit[1])