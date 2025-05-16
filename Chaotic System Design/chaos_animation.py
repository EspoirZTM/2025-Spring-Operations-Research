import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# ---------- Step 1: 定义 Scholar-Chaos 系统 ----------
def scholar_chaos(t, state, alpha=10, beta=8, gamma=3, mu=2, nu=1, eta=1):
    x, y, z = state
    dx = alpha * (y - x) + mu * np.sin(z)
    dy = beta * x - y - x * z + nu * np.cos(x)
    dz = x * y - gamma * z + eta * np.sin(y)
    return [dx, dy, dz]

# ---------- Step 2: 设置初始条件与求解 ----------
initial_conditions = [
    [1, 1, 1],
    [1.01, 1.01, 1.01],
    [-1, -1, 0.5],
    [2, -1, 2],
    [-4, 2, -1]
]

t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], 2000)
solutions = []

for ic in initial_conditions:
    sol = solve_ivp(scholar_chaos, t_span, ic, t_eval=t_eval,
                    args=(10, 8, 3, 2, 1, 1), rtol=1e-8, atol=1e-10)
    solutions.append(sol)

# ---------- Step 3: 创建动画 ----------
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
colors = ['r', 'g', 'b', 'm', 'orange']

lines = [ax.plot([], [], [], color=color, label=f'IC={ic}')[0]
         for ic, color in zip(initial_conditions, colors)]

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-5, 15)
ax.set_title("Zhu-Chaos System Animation", fontsize=15)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.legend()

def update(frame):
    for line, sol in zip(lines, solutions):
        line.set_data(sol.y[0][:frame], sol.y[1][:frame])
        line.set_3d_properties(sol.y[2][:frame])
    return lines

ani = FuncAnimation(fig, update, frames=len(t_eval), interval=20, blit=False)

plt.tight_layout()
plt.show()
