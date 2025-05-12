import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 定义洛伦兹方程
def lorenz(t, state, sigma, rho, beta):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# 参数和初始条件
sigma, rho, beta = 10, 28, 8/3
initial_state = [1.0, 1.0, 1.0]
t_span = (0, 50)
t_eval = np.linspace(0, 50, 10000)

# 解方程
sol = solve_ivp(lorenz, t_span, initial_state, args=(sigma, rho, beta), t_eval=t_eval)

# 画相图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(sol.y[0], sol.y[1], sol.y[2], lw=0.5)
ax.set_xlabel('X'), ax.set_ylabel('Y'), ax.set_zlabel('Z')
plt.show()
