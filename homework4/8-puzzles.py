import random
import math

acc1 = 0
acc2 = 0
acc3 = 0
acc4 = 0

# 生成一个初始的8数码状态，0表示空格
def generate_8puzzle():
    puzzle = list(range(1, 9)) + [0]
    for _ in range(100):  # 打乱100次
        idx1, idx2 = random.sample(range(9), 2)
        puzzle[idx1], puzzle[idx2] = puzzle[idx2], puzzle[idx1]
    return puzzle

# 打印八数码问题的状态
def print_puzzle(puzzle):
    for i in range(0, len(puzzle), 3):
        print(" ".join(str(x) if x != 0 else ' ' for x in puzzle[i:i+3]))

# 计算曼哈顿距离作为代价函数
def manhattan_distance(puzzle, goal):
    distance = 0
    for i in range(9):
        if puzzle[i] != 0:
            correct_row, correct_col = divmod(goal.index(puzzle[i]), 3)
            current_row, current_col = divmod(i, 3)
            distance += abs(correct_row - current_row) + abs(correct_col - current_col)
    return distance

# 生成一个新的邻居状态
def get_neighbors(puzzle):
    zero_index = puzzle.index(0)
    row, col = divmod(zero_index, 3)
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 上下左右移动
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_puzzle = list(puzzle)
            new_puzzle[zero_index], new_puzzle[new_row * 3 + new_col] = new_puzzle[new_row * 3 + new_col], new_puzzle[zero_index]
            neighbors.append(new_puzzle)
    return neighbors

# 最陡上升爬山法
def steepest_ascent_hill_climbing(puzzle, goal, max_iterations=100):
    current_puzzle = list(puzzle)
    best_puzzle = list(puzzle)
    best_distance = manhattan_distance(puzzle, goal)
    iterations = 0
    while iterations < max_iterations:
        neighbors = get_neighbors(current_puzzle)
        best_neighbor = None
        min_distance = float('inf')
        for neighbor in neighbors:
            distance = manhattan_distance(neighbor, goal)
            if distance < min_distance:
                best_neighbor = neighbor
                min_distance = distance
        if best_neighbor is not None and min_distance < best_distance:
            best_distance = min_distance
            best_puzzle = list(best_neighbor)
            current_puzzle = best_neighbor
        else:
            break
        iterations += 1
    return best_puzzle, iterations

# 首选爬山法
def first_choice_hill_climbing(puzzle, goal, max_iterations=100):
    current_puzzle = list(puzzle)
    best_puzzle = list(puzzle)
    best_distance = manhattan_distance(puzzle, goal)
    iterations = 0
    while iterations < max_iterations:
        neighbors = get_neighbors(current_puzzle)
        if not neighbors:
            break
        for neighbor in neighbors:
            distance = manhattan_distance(neighbor, goal)
            if distance < best_distance:
                best_distance = distance
                best_puzzle = list(neighbor)
                current_puzzle = list(neighbor)
                break  # 一旦找到更好的邻居，立即接受它
        iterations += 1
    return best_puzzle, iterations

# 随机重启爬山法
def random_restart_hill_climbing(goal, max_restarts=1000, max_iterations=100):
    restarts = 0
    while restarts < max_restarts:
        # 从一个随机初始状态开始
        initial_puzzle = generate_8puzzle()
        solution, iterations = steepest_ascent_hill_climbing(initial_puzzle, goal, max_iterations)
        
        # 如果找到了目标状态，返回解
        if solution == goal:
            # print(f"Solution found after {restarts + 1} restarts and {iterations} iterations.")
            return 1
        
        restarts += 1
    
    # print("Solution not found within the given restarts.")
    return 0

# 模拟退火算法
def simulated_annealing(goal, initial_temp=10000, min_temp=1, alpha=0.99, max_iterations=1000):
    current_puzzle = generate_8puzzle()
    current_distance = manhattan_distance(current_puzzle, goal)
    temperature = initial_temp
    iteration = 0
    
    while temperature > min_temp and iteration < max_iterations:
        neighbors = get_neighbors(current_puzzle)
        new_puzzle = random.choice(neighbors)
        new_distance = manhattan_distance(new_puzzle, goal)
        
        # 计算接受新状态的概率
        if new_distance < current_distance:
            current_puzzle = new_puzzle
            current_distance = new_distance
        else:
            delta = current_distance - new_distance
            acceptance_prob = math.exp(delta / temperature)
            if random.random() < acceptance_prob:
                current_puzzle = new_puzzle
                current_distance = new_distance
        
        # 降温
        temperature *= alpha
        iteration += 1
    
    return current_puzzle, current_distance, iteration


# 模拟退火算法
def simulated_annealing2(goal, initial_temp=1000000, cooling_rate=0.99999, min_temp=1):
    current_puzzle = generate_8puzzle()
    current_distance = manhattan_distance(current_puzzle, goal)
    best_puzzle = list()
    best_distance = current_distance
    temperature = initial_temp
    
    while temperature > min_temp:
        neighbor = random.choice(get_neighbors(current_puzzle))
        neighbor_distance = manhattan_distance(neighbor, goal)
        
        if neighbor_distance < current_distance:  # 如果找到了更好的解
            current_puzzle = neighbor
            current_distance = neighbor_distance
            if neighbor_distance < best_distance:  # 更新最佳解
                best_puzzle = neighbor
                best_distance = neighbor_distance
        elif random.random() < math.exp((current_distance - neighbor_distance) / temperature):  # 接受较差的解
            current_puzzle = neighbor
            current_distance = neighbor_distance
        
        temperature *= cooling_rate  # 降温
    
    return best_distance == 0

# 八数码问题的目标状态
goal_puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# # 生成一个初始状态
# initial_puzzle = generate_8puzzle()
# print("Initial Puzzle:")
# print_puzzle(initial_puzzle)

# # 使用最陡上升爬山法求解
# solution, iterations = steepest_ascent_hill_climbing(initial_puzzle, goal_puzzle)
# print("\nSolution by Steepest Ascent Hill Climbing:")
# print_puzzle(solution)
# print(f"Iterations: {iterations}")

# # 使用首选爬山法求解
# solution, iterations = first_choice_hill_climbing(initial_puzzle, goal_puzzle)
# print("\nSolution by First Choice Hill Climbing:")
# print_puzzle(solution)
# print(f"Iterations: {iterations}")

for i in range(100):
    # initial_puzzle = generate_8puzzle()
    # if goal_puzzle == steepest_ascent_hill_climbing(initial_puzzle, goal_puzzle):
    #     acc1 += 1
    # if goal_puzzle == first_choice_hill_climbing(initial_puzzle, goal_puzzle):
    #     acc2 += 1
    acc3 += random_restart_hill_climbing(goal_puzzle)
    # 使用模拟退火算法求解
    # solution, distance, iterations = simulated_annealing(goal_puzzle)

    # print(f"Solution found with final distance {distance} after {iterations} iterations.")
    # print_puzzle(solution)
    # acc4 += simulated_annealing2(goal_puzzle)


# print(acc1/100)
# print(acc2/100)
print(acc3/100)
# print(acc4)


