'''
Author: shysgsg 1054733568@qq.com
Date: 2024-12-06 22:48:27
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2024-12-06 23:03:00
FilePath: \人工智能\8-queens.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import random
import math
import time

# 生成一个随机解
def generate_initial_state(n=8):
    # 随机放置 n 个皇后，每个皇后在不同的列
    return [random.randint(0, n-1) for _ in range(n)]

# 计算当前状态的代价：皇后之间的冲突数
def calculate_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                conflicts += 1
    return conflicts

# 获取邻居状态：通过在某一列中移动皇后来生成邻居
def get_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        # 尝试将皇后从当前行移动到其他行
        for row in range(n):
            if row != state[col]:  # 不和当前行重合
                neighbor = state[:]
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

# 最陡上升爬山法（Steepest-Ascent Hill Climbing）
def steepest_ascent_hill_climbing(n=8):
    current_state = generate_initial_state(n)
    current_conflicts = calculate_conflicts(current_state)
    
    while True:
        neighbors = get_neighbors(current_state)
        next_state = None
        next_conflicts = current_conflicts
        
        # 选择代价最小的邻居
        for neighbor in neighbors:
            conflict_count = calculate_conflicts(neighbor)
            if conflict_count < next_conflicts:
                next_state = neighbor
                next_conflicts = conflict_count
        
        # 如果没有找到更优解，退出
        if next_conflicts >= current_conflicts:
            break
        current_state = next_state
        current_conflicts = next_conflicts
    
    return current_state, current_conflicts

# 首选爬山法（First-Choice Hill Climbing）
def first_choice_hill_climbing(n=8):
    current_state = generate_initial_state(n)
    current_conflicts = calculate_conflicts(current_state)
    
    while True:
        neighbors = get_neighbors(current_state)
        random.shuffle(neighbors)  # 随机打乱邻居顺序，增加多样性
        
        for neighbor in neighbors:
            conflict_count = calculate_conflicts(neighbor)
            if conflict_count < current_conflicts:
                current_state = neighbor
                current_conflicts = conflict_count
                break
        else:
            # 如果没有找到更好的邻居，退出
            break
    
    return current_state, current_conflicts

# 随机重启爬山法（Random Restart Hill Climbing）
def random_restart_hill_climbing(n=8, max_restarts=100):
    restart_count = 0
    best_state = None
    best_conflicts = float('inf')
    
    while restart_count < max_restarts:
        restart_count += 1
        # print(f"Restart #{restart_count}")
        
        # 使用最陡上升爬山法进行搜索
        current_state, current_conflicts = steepest_ascent_hill_climbing(n)
        
        # 更新全局最优解
        if current_conflicts < best_conflicts:
            best_state = current_state
            best_conflicts = current_conflicts
        
        # 如果找到了冲突为0的解，提前终止
        if best_conflicts == 0:
            break
    
    return best_state, best_conflicts

# 模拟退火算法
def simulated_annealing(n=8, initial_temp=1000, cooling_rate=0.995, max_iterations=10000):
    current_state = generate_initial_state(n)
    current_conflicts = calculate_conflicts(current_state)
    best_state = current_state[:]
    best_conflicts = current_conflicts
    temperature = initial_temp
    
    iteration = 0
    while iteration < max_iterations and temperature > 0.1:
        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        next_conflicts = calculate_conflicts(next_state)
        
        # 如果下一个状态更好（冲突更少），或者以一定概率接受较差的解
        if next_conflicts < current_conflicts or random.random() < math.exp((current_conflicts - next_conflicts) / temperature):
            current_state = next_state
            current_conflicts = next_conflicts
        
        # 更新最优解
        if current_conflicts < best_conflicts:
            best_state = current_state[:]
            best_conflicts = current_conflicts
        
        # 降低温度
        temperature *= cooling_rate
        iteration += 1
        
        # 如果已经找到完美解，提前终止
        if best_conflicts == 0:
            break
    
    return best_state, best_conflicts

# 打印棋盘状态
def print_board(state):
    n = len(state)
    for row in range(n):
        board_row = ['Q' if col == state[row] else '.' for col in range(n)]
        print(" ".join(board_row))
    print("\n")

# # 运行最陡上升爬山法
# solution, conflicts = steepest_ascent_hill_climbing()
# print("Steepest-Ascent Hill Climbing Solution (conflicts =", conflicts, "):")
# print_board(solution)

# # 运行首选爬山法
# solution, conflicts = first_choice_hill_climbing()
# print("First-Choice Hill Climbing Solution (conflicts =", conflicts, "):")
# print_board(solution)

# # 运行随机重启爬山法
# solution, conflicts = random_restart_hill_climbing()
# print("Random Restart Hill Climbing Solution (conflicts =", conflicts, "):")
# print_board(solution)

# # 运行模拟退火算法
# solution, conflicts = simulated_annealing()
# print("Simulated Annealing Solution (conflicts =", conflicts, "):")
# print_board(solution)

# 用于计时的辅助函数
def time_function(func, *args):
    start_time = time.time()
    for _ in range(1000):
        result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

# 比较三种方法的执行时间
def compare_methods():
    # 1. 最陡上升爬山法
    result, time_1 = time_function(steepest_ascent_hill_climbing)
    print(f"steepest_ascent_hill_climbing Time: {time_1:.4f} seconds")

    # 2. 首选爬山法
    result, time_2 = time_function(first_choice_hill_climbing)
    print(f"first_choice_hill_climbing Time: {time_2:.4f} seconds")

    # 3. 随机重启爬山法
    result, time_3 = time_function(random_restart_hill_climbing)
    print(f"random_restart_hill_climbing Time: {time_3:.4f} seconds")

     # 4. 模拟退火算法
    result, time_4 = time_function(simulated_annealing)
    print(f"simulated_annealing Time: {time_4:.4f} seconds")

# 运行比较
compare_methods()
