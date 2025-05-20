import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import matplotlib
# 配置 matplotlib 使用中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 你可以使用 'Microsoft YaHei' 或其他中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# Data setup
nodes = [1, 2, 3, 4, 5, 6, 7]
populations = {1: 34, 2: 29, 3: 42, 4: 21, 5: 56, 6: 18, 7: 71}
adjacency = {
    1: [2, 3],
    2: [1, 3, 4],
    3: [1, 4],
    4: [2, 3, 5, 6, 7],
    5: [2, 4, 6],
    6: [4, 5, 7],
    7: [4, 6]
}

# Brute-force search for optimal placement and coverage
best = {'pair': None, 'covers': None, 'total_pop': 0}

for i, k in itertools.combinations(nodes, 2):
    choices_i = adjacency[i] + [None]
    choices_k = adjacency[k] + [None]
    for j in choices_i:
        for l in choices_k:
            covered = {i, k}
            if j: covered.add(j)
            if l: covered.add(l)
            total = sum(populations[n] for n in covered)
            if total > best['total_pop']:
                best = {'pair': (i, k), 'covers': (j, l), 'total_pop': total}

# Extract best result
(i, k) = best['pair']
(j, l) = best['covers']
covered_nodes = {i, k} | ({j} if j else set()) | ({l} if l else set())

# Prepare DataFrame
df = pd.DataFrame({
    'Facility Node': [i, k],
    'Covered Adjacent': [j if j else 'None', l if l else 'None']
})

# Display result
print("最佳销售代理安排")
print(df)
print(f"\n最大覆盖学生人数: {best['total_pop']}k")# Visualization
G = nx.Graph(adjacency)
pos = nx.spring_layout(G, seed=42)


# Visualization with enhanced features
G = nx.Graph(adjacency)
pos = nx.spring_layout(G, seed=42)

# 定义节点颜色和大小
facility_color = '#FF5733'  # 红色代表设施节点
covered_color = '#33A1FF'   # 蓝色代表覆盖节点
other_color = '#D3D3D3'     # 灰色代表其他节点

node_colors = []
node_sizes = []
for n in nodes:
    if n in (i, k):
        node_colors.append(facility_color)
        node_sizes.append(1000)
    elif n in covered_nodes:
        node_colors.append(covered_color)
        node_sizes.append(800)
    else:
        node_colors.append(other_color)
        node_sizes.append(600)

# 添加边权重（这里使用相邻节点人口之和作为权重）
edge_weights = []
for u, v in G.edges():
    edge_weights.append(populations[u] + populations[v])

# 绘制图形
plt.figure(figsize=(10, 8))

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)

# 绘制边（根据权重设置宽度）
nx.draw_networkx_edges(G, pos, width=[w/50 for w in edge_weights],
                      edge_color='#888888', alpha=0.6)

# 绘制标签（添加人口数据）
labels = {n: f"{n}\n({populations[n]}k)" for n in nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=10)

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='设施节点',
           markerfacecolor=facility_color, markersize=10),
    Line2D([0], [0], marker='o', color='w', label='覆盖节点',
           markerfacecolor=covered_color, markersize=10),
    Line2D([0], [0], marker='o', color='w', label='其他节点',
           markerfacecolor=other_color, markersize=10),
    Line2D([0], [0], color='#888888', lw=2, label='边权重')
]
plt.legend(handles=legend_elements, loc='upper right')

# 添加标题和说明
plt.title("最佳销售代理点安排", fontsize=14, y=1.05)

plt.text(0.5, -0.1, f"Facility nodes cover themselves and adjacent nodes\n"
        f"Edge width represents combined population of connected nodes",
        ha='center', transform=plt.gca().transAxes)

plt.tight_layout()
plt.show()
