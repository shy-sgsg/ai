import networkx as nx

# 创建一个图来表示澳大利亚各区域的相邻关系
G = nx.Graph()

# 添加节点，对应各个州和领地
regions = ["WA", "NT", "Q", "SA", "NSW", "V", "T"]
G.add_nodes_from(regions)

# 添加边，来表示相邻关系
G.add_edges_from([("WA", "NT"), ("WA", "SA"), ("NT", "Q"), ("NT", "SA"),
                  ("Q", "NSW"), ("Q", "SA"), ("NSW", "V"), ("NSW", "SA"),
                  ("V", "SA"), ("T", "V")])

# 定义三种颜色
colors = ["r", "g", "b"]

# 用于记录所有有效的着色方案
all_colorings = []


# 定义一个递归函数来进行穷举着色
def enumerate_colorings(current_region_index, coloring):
    if current_region_index == len(regions):
        all_colorings.append(coloring.copy())
        return
    region = regions[current_region_index]
    used_colors = []
    neighbors = list(G.neighbors(region))
    for neighbor in neighbors:
        if coloring[neighbor] is not None:
            used_colors.append(coloring[neighbor])
    for color in colors:
        if color not in used_colors:
            coloring[region] = color
            enumerate_colorings(current_region_index + 1, coloring)
            coloring[region] = None


# 初始的着色字典，初始化为None
initial_coloring = {region: None for region in regions}
enumerate_colorings(0, initial_coloring)

print(f"总共有 {len(all_colorings)} 种不同的有效着色方案（解）。")