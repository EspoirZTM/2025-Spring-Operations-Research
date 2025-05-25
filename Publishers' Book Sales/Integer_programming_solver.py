import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import matplotlib

# 配置 matplotlib 使用中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# Data setup
nodes = [1, 2, 3, 4, 5, 6, 7]
populations = {1: 34, 2: 29, 3: 42, 4: 21, 5: 56, 6: 18, 7: 71}
adjacency = {
    1: [2, 3],
    2: [1, 3, 4],
    3: [1,2,4],
    4: [2, 3, 5, 6, 7],
    5: [2, 4, 6],
    6: [4, 5, 7],
    7: [4, 6]
}

# 创建DataFrame存储所有中间结果
all_results = pd.DataFrame(columns=['设施节点1', '设施节点2', '覆盖节点1', '覆盖节点2', '覆盖总人数'])

# Brute-force search for optimal placement and coverage
best = {'pair': None, 'covers': None, 'total_pop': 0}

print("开始计算所有可能的设施节点组合及其覆盖情况...")
for i, k in itertools.combinations(nodes, 2):
    choices_i = adjacency[i] + [None]
    choices_k = adjacency[k] + [None]
    for j in choices_i:
        for l in choices_k:
            covered = {i, k}
            if j: covered.add(j)
            if l: covered.add(l)
            total = sum(populations[n] for n in covered)

            # 记录当前组合到中间结果
            new_row = {
                '设施节点1': i,
                '设施节点2': k,
                '覆盖节点1': j if j else '无',
                '覆盖节点2': l if l else '无',
                '覆盖总人数': total
            }
            all_results = pd.concat([all_results, pd.DataFrame([new_row])], ignore_index=True)

            if total > best['total_pop']:
                best = {'pair': (i, k), 'covers': (j, l), 'total_pop': total}

# 输出所有中间结果
print("\n所有可能的设施节点组合及其覆盖情况:")
print(all_results.sort_values(by='覆盖总人数', ascending=False).reset_index(drop=True))

# Extract best result
(i, k) = best['pair']
(j, l) = best['covers']
covered_nodes = {i, k} | ({j} if j else set()) | ({l} if l else set())

# Prepare DataFrame for best result
df = pd.DataFrame({
    'Facility Node': [i, k],
    'Covered Adjacent': [j if j else 'None', l if l else 'None']
})

# Display best result
print("\n最佳销售代理安排")
print(df)
print(f"\n最大覆盖学生人数: {best['total_pop']}k")

# Visualization (保持不变)
G = nx.Graph(adjacency)
pos = nx.spring_layout(G, seed=42)

# 定义节点颜色和大小
facility_color = '#FF5733'
covered_color = '#33A1FF'
other_color = '#D3D3D3'

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

edge_weights = []
for u, v in G.edges():
    edge_weights.append(populations[u] + populations[v])

plt.figure(figsize=(10, 8))
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)
nx.draw_networkx_edges(G, pos, width=[w / 50 for w in edge_weights],
                       edge_color='#888888', alpha=0.6)

labels = {n: f"{n}\n({populations[n]}k)" for n in nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=10)

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



plt.tight_layout()
plt.savefig('Integer_programming_solver.pdf')
plt.show()
