import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import itertools

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

# Display result - 修改后的部分
print("Optimal Sales Agents Placement")
print(df)
print(f"\n最大覆盖学生人数: {best['total_pop']}k")# Visualization
G = nx.Graph(adjacency)
pos = nx.spring_layout(G, seed=42)

# Node sizes: facility = 600, covered = 400, others = 200
node_sizes = []
for n in nodes:
    if n in (i, k):
        node_sizes.append(600)
    elif n in covered_nodes:
        node_sizes.append(400)
    else:
        node_sizes.append(200)

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=node_sizes)
plt.title(f"Optimal Placement: Nodes {i} & {k}, Covers {best['total_pop']}k Students")
plt.show()