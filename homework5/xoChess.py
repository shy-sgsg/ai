# 检查当前棋盘是否是一个合法的状态
def is_legal(board):
    # 统计 X 和 O 的数量
    x_count = board.count('X')
    o_count = board.count('O')

    # X 的数量必须大于等于 O 的数量，且 X 的数量最多只能比 O 多 1
    if not (x_count == o_count or x_count == o_count + 1):
        return False

    # 检查是否有任何一方已经胜利，如果有，另一个玩家不能下棋
    if check_win(board, 'X') and x_count == o_count:
        return False  # 如果 X 胜利，X 的数量必须比 O 多 1
    if check_win(board, 'O') and x_count > o_count:
        return False  # 如果 O 胜利，O 的数量必须等于 X

    return True


def check_win(board, player):
    lines = []
    # 横向检查
    for i in range(3):
        lines.append(board[i])
    # 纵向检查
    for i in range(3):
        lines.append([board[j][i] for j in range(3)])
    # 对角线检查
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])
    
    for line in lines:
        if line == [player, player, player]:
            return True
    return False

# 遍历所有合法的井字棋状态
def generate_all_legal_boards(board, player, legal_boards_set):
    # 将 board 转换为元组，因为列表是不可哈希的
    board_tuple = tuple(board)

    # 如果当前棋盘是合法的且没有更多的棋可以下，添加到合法状态列表
    if is_legal(board):
        legal_boards_set.add(board_tuple)  # 使用集合避免重复的棋盘
    
    # 递归生成所有可能的下一步棋局
    for i in range(9):
        if board[i] == ' ':
            new_board = list(board)  # 将当前列表转换为列表
            new_board[i] = player  # 当前玩家下棋
            new_player = 'O' if player == 'X' else 'X'  # 切换玩家
            generate_all_legal_boards(new_board, new_player, legal_boards_set)

def print_board(board):
    for row in board:
        print(row)
    print()

def count_x_o_line(line):
    X_count = line.count('X')
    O_count = line.count('O')
    return X_count, O_count

def eval_terminal_state(board):
    if check_win(board, 'X'):
        return 1  # X wins
    if check_win(board, 'O'):
        return -1  # O wins
    return 0  # No winner yet

def evaluate(board):
    terminal_eval = eval_terminal_state(board)
    if terminal_eval != 0:
        return terminal_eval
    
    X_1 = X_2 = O_1 = O_2 = 0
    lines = []
    # 横向行
    for i in range(3):
        lines.append(board[i])
    # 纵向列
    for i in range(3):
        lines.append([board[j][i] for j in range(3)])
    # 对角线
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])

    for line in lines:
        X_count, O_count = count_x_o_line(line)
        if X_count == 3:
            X_2 += 1
        elif X_count == 2:
            X_2 += 1
        elif X_count == 1:
            X_1 += 1
        if O_count == 3:
            O_2 += 1
        elif O_count == 2:
            O_2 += 1
        elif O_count == 1:
            O_1 += 1
    eval_value = 3 * X_2 + X_1 - (3 * O_2 + O_1)
    return eval_value

def generate_game_tree(board, player, depth):
    if depth == 0:
        return evaluate(board)  # 基础评估（不再继续生成树）
    
    next_player = 'O' if player == 'X' else 'X'
    evaluations = []
    
    # 遍历每个空位置，生成新的状态
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                new_board = [row[:] for row in board]  # 深拷贝
                new_board[i][j] = player
                print_board(new_board)
                evaluation = generate_game_tree(new_board, next_player, depth - 1)
                evaluations.append((new_board, evaluation))  # 存储评估值
    
    for board_state, eval_value in evaluations:
        print(f"board state: \n{board_state}\n evaluations: {eval_value}\n")
    
    # 选择最优评估值
    if player == 'X':
        return max(evaluations, key=lambda x: x[1])[1]
    else:
        return min(evaluations, key=lambda x: x[1])[1]
    
# 主程序
def main():
    # 初始化棋盘为空格
    board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]  # 3x3 的棋盘，用字符串表示，空格表示未下棋
    # legal_boards_set = set()  # 使用集合来存储合法状态，避免重复
    # 生成所有合法状态
    # generate_all_legal_boards(board, 'X', legal_boards_set)
    # 输出合法状态的数量
    # print(len(legal_boards_set))
    # # 生成深度为2的博弈树
    # generate_game_tree(board, 'X', 2)
    # 生成深度为2的博弈树并评估每个棋局
    evaluate_value = generate_game_tree(board, 'X', 2)
    # print(evaluate_value)


if __name__ == "__main__":
    main()
