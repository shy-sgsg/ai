'''
Author: shysgsg 1054733568@qq.com
Date: 2024-12-08 17:02:22
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2024-12-08 20:53:21
FilePath: \人工智能\goRiver.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from collections import deque

# 定义状态，其中M表示传教士，C表示野人，0表示在起始岸，1表示在对岸
# 状态是一个包含6个元素的元组，分别表示三个传教士和三个野人在哪个岸
# 0表示起始岸，1表示对岸

def is_valid(state):
    # 检查当前状态是否有效
    left = state.count(0)
    right = 3 - left
    for i in [0, 1]:
        if state[i] + state[i+3] > left:
            return False
        if state[i+3] > right:
            return False
    return True

def next_states(state):
    # 产生下一个状态
    for i in range(6):
        if i < 3 and state[i] == 0:  # 传教士或野人在起始岸
            yield (state[:i] + (1,) + state[i+1:] + (0,) + state[4:])
        if i < 3 and state[i+3] == 0:  # 传教士或野人在对岸
            yield (state[:i] + (0,) + state[i+1:] + (1,) + state[4:])

def bfs():
    # 广度优先搜索
    queue = deque([(0,0,0,0,0,0)])  # 初始状态，所有传教士和野人都起始岸
    visited = set()
    result = []
    while queue:
        state = queue.popleft()
        if state not in visited:
            visited.add(state)
            if state == (1,1,1,1,1,1):  # 目标状态，所有人都在对岸
                result.append(state)
            for next_state in next_states(state):
                if next_state not in visited and is_valid(next_state):
                    queue.append(next_state)
    return result

# 执行BFS并打印结果
results = bfs()
for i, state in enumerate(results):
    print(f"State {i+1}: {state}")

# 打印状态转换图
print("\nState Transition Graph:")
for i, state in enumerate(results):
    for j, next_state in enumerate(results):
        if state != next_state and any(s != t for s, t in zip(state, next_state)):
            print(f"State {state} -> State {next_state}")



