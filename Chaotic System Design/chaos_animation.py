import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 修改后的 Rössler 系统
def modified_rossler(t, state, a=0.2, b=0.2, c=5.7, alpha=0.1, beta=0.1):
    x, y, z = state
    dx = -y - z + alpha * np.sin(z)
    dy = x + a * y
    dz = b + z*(x - c) + beta * np.cos(x)
    return [dx, dy, dz]

# 动画参数设置
FRAMES = 100  # 总帧数
INTERVAL = 20  # 帧间隔(ms)
TRAIL_LENGTH = 100  # 轨迹尾迹长度

# 初始化图形
fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(projection='3d')

# 初始化图形元素
lines = []
for i in range(3):
    line3d, = ax1.plot([], [], [], lw=0.5, alpha=0.6)
    lines.append(line3d)

# 解决求解器输出时间点不均匀的问题
def uniform_sampling(sol, total_frames):
    t = sol.t
    y = sol.y
    new_t = np.linspace(t[0], t[-1], total_frames)
    new_y = np.array([np.interp(new_t, t, row) for row in y])
    return new_t, new_y

initial_conditions = [
    [1.0, 2.0, 3.0],  # 第一个初始条件
    [4.0, 5.0, 6.0],  # 第二个初始条件
    [7.0, 8.0, 9.0]   # 第三个初始条件
]
# 定义时间范围
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 100)
# 预处理数据
solutions = []
for ic in initial_conditions:
    sol = solve_ivp(modified_rossler, t_span, ic, t_eval=t_eval,
                    args=(0.2, 0.2, 5.7, 0.1, 0.1), rtol=1e-8, atol=1e-10)
    t, y = uniform_sampling(sol, FRAMES)  # 均匀采样
    solutions.append((t, y))

# 动画更新函数
def update(frame):
    for idx, (t, y) in enumerate(solutions):
        # 获取当前轨迹数据
        start_idx = max(0, frame - TRAIL_LENGTH)
        x = y[0, start_idx:frame+1]
        y_vals = y[1, start_idx:frame+1]
        z = y[2, start_idx:frame+1]

        # 更新3D相图
        lines[idx].set_data(x, y_vals)
        lines[idx].set_3d_properties(z)

    # 实时更新坐标范围（仅演示第一个解）
    current_x = solutions[0][1][0, max(0,frame-100):frame+1]
    current_y = solutions[0][1][1, max(0,frame-100):frame+1]
    current_z = solutions[0][1][2, max(0,frame-100):frame+1]

    ax1.set_xlim(current_x.min()-1, current_x.max()+1)
    ax1.set_ylim(current_y.min()-1, current_y.max()+1)
    ax1.set_zlim(current_z.min()-1, current_z.max()+1)

    return lines

# 初始化函数
def init():
    ax1.set_xlim(-20, 20)
    ax1.set_ylim(-20, 20)
    ax1.set_zlim(0, 20)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")

    return lines

# 创建动画
ani = FuncAnimation(fig, update, frames=FRAMES,
                    init_func=init, blit=True,
                    interval=INTERVAL)

# 保存动画（需要ffmpeg）
# ani.save('rossler_animation.mp4', writer='ffmpeg', fps=30)

plt.show()
