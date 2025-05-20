import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def scholar_chaos(t, state, alpha=10, beta=8, gamma=3, mu=2, nu=1, eta=1):
    x, y, z = state
    dx = alpha * (y - x) + mu * np.sin(z)
    dy = beta * x - y - x * z + nu * np.cos(x)
    dz = x * y - gamma * z + eta * np.sin(y)
    return [dx, dy, dz]

# 初始条件列表
initial_conditions = [
    [1.0, 1.0, 1.0],
    [1.1, 1.1, 1.1],
    [2.0, -1.5, 1.5],
    [-1.0, 2.0, -1.0]
]

# 求解系统
t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], 5000)
solutions = []
for ic in initial_conditions:
    sol = solve_ivp(scholar_chaos, t_span, ic, t_eval=t_eval,
                    args=(10, 8, 3, 2, 1, 1), rtol=1e-8, atol=1e-10)
    solutions.append(sol)

# 创建组合大图
plt.figure(figsize=(15, 12))  # 增大画布尺寸
colors = ['r', 'g', 'b', 'm']

# 1. 3D相图
ax1 = plt.subplot(221, projection='3d')
for sol, color, ic in zip(solutions, colors, initial_conditions):
    ax1.plot(sol.y[0], sol.y[1], sol.y[2], color=color, label=f"IC={ic}")
ax1.set_title("(a) 3D Phase Portrait")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")
ax1.legend(prop={'size': 8})

# 2. x-y投影
ax2 = plt.subplot(222)
for sol, color in zip(solutions, colors):
    ax2.plot(sol.y[0], sol.y[1], color=color)
ax2.set_title("(b) x-y Projection")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.grid(True)

# 3. x-z投影
ax3 = plt.subplot(223)
for sol, color in zip(solutions, colors):
    ax3.plot(sol.y[0], sol.y[2], color=color)
ax3.set_title("(c) x-z Projection")
ax3.set_xlabel("x")
ax3.set_ylabel("z")
ax3.grid(True)

# 4. 时间序列
ax4 = plt.subplot(224)
sol = solutions[0]
ax4.plot(sol.t, sol.y[0], label="x(t)", color='r')
ax4.plot(sol.t, sol.y[1], label="y(t)", color='g')
ax4.plot(sol.t, sol.y[2], label="z(t)", color='b')
ax4.set_title("(d) Time Series")
ax4.set_xlabel("Time t")
ax4.set_ylabel("States")
ax4.legend()
ax4.grid(True)

# 调整布局并保存
plt.tight_layout(pad=3.0)  # 增加子图间距
# plt.savefig("Zhu_Chaos_Combined.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.show()
