'''
Author: shysgsg 1054733568@qq.com
Date: 2024-12-08 23:14:54
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2024-12-08 23:27:29
FilePath: \人工智能\homework5\1.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 假设我们已经有了评估函数
def eval_board(board):
    X2 = O2 = X1 = O1 = 0
    # 行列和对角线上的X和O的数量
    for i in range(3):
        row = board[i]
        col = [board[j][i] for j in range(3)]
        
        # 检查行
        if row.count('X') == 2 and row.count('O') == 0: X2 += 1
        if row.count('O') == 2 and row.count('X') == 0: O2 += 1
        if row.count('X') == 1 and row.count('O') == 0: X1 += 1
        if row.count('O') == 1 and row.count('X') == 0: O1 += 1
        
        # 检查列
        if col.count('X') == 2 and col.count('O') == 0: X2 += 1
        if col.count('O') == 2 and col.count('X') == 0: O2 += 1
        if col.count('X') == 1 and col.count('O') == 0: X1 += 1
        if col.count('O') == 1 and col.count('X') == 0: O1 += 1
    
    # 对角线检查
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2-i] for i in range(3)]
    for diag in [diag1, diag2]:
        if diag.count('X') == 2 and diag.count('O') == 0: X2 += 1
        if diag.count('O') == 2 and diag.count('X') == 0: O2 += 1
        if diag.count('X') == 1 and diag.count('O') == 0: X1 += 1
        if diag.count('O') == 1 and diag.count('X') == 0: O1 += 1
    
    return 3*X2 + X1 - (3*O2 + O1)

# 初始化游戏树的节点
class Node:
    def __init__(self, board, is_maximizing_player, depth):
        self.board = board  # 当前棋盘状态
        self.is_maximizing_player = is_maximizing_player  # 是否是最大化玩家
        self.depth = depth  # 当前节点的深度
        self.children = []  # 子节点
        self.value = None  # 节点的值（评估值）
        self.alpha = -float('inf')  # 最大值
        self.beta = float('inf')  # 最小值

# 生成子节点（简单的棋盘状态生成，假设不考虑有效性检查）
def generate_children(node):
    if node.depth >= 2:  # 限制深度
        return []
    
    # 假设所有空白位置都可以填X或O
    board = node.board
    children = []
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                new_board = [row.copy() for row in board]  # 复制棋盘
                new_board[i][j] = 'X' if node.is_maximizing_player else 'O'
                children.append(Node(new_board, not node.is_maximizing_player, node.depth + 1))
    
    return children

# Alpha-beta 剪枝算法
def alpha_beta(node, alpha, beta):
    if node.depth == 2:  # 到达深度 2，返回评估值
        node.value = eval_board(node.board)
        return node.value
    
    if node.is_maximizing_player:
        max_eval = -float('inf')
        for child in generate_children(node):
            eval_value = alpha_beta(child, alpha, beta)
            max_eval = max(max_eval, eval_value)
            alpha = max(alpha, eval_value)
            if beta <= alpha:  # 剪枝
                print(f"cut off:{child.board}")
                break
        node.value = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child in generate_children(node):
            eval_value = alpha_beta(child, alpha, beta)
            min_eval = min(min_eval, eval_value)
            beta = min(beta, eval_value)
            if beta <= alpha:  # 剪枝
                print(f"cut off:{child.board}")
                break
        node.value = min_eval
        return min_eval

# 初始化一个棋盘状态
initial_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
root = Node(initial_board, True, 0)  # 假设X是最大化玩家

# 执行alpha-beta剪枝
alpha_beta(root, -float('inf'), float('inf'))

