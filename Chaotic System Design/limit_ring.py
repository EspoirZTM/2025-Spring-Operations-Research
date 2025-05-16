import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def scholar_chaos(t, state, alpha=10, beta=8, gamma=3, mu=2, nu=1, eta=1):
    x, y, z = state
    dx = alpha * (y - x) + mu * np.sin(z)
    dy = beta * x - y - x * z + nu * np.cos(x)
    dz = x * y - gamma * z + eta * np.sin(y)
    return [dx, dy, dz]

def jacobian(x, y, z, alpha, beta, gamma, mu, nu, eta):
    return np.array([
        [-alpha, alpha, mu * np.cos(z)],
        [beta - z - nu * np.sin(x), -1, -x],
        [y, x + eta * np.cos(y), -gamma]
    ])

def compute_max_lyapunov(ic, t_max=100, dt=0.01, renormalization_interval=10,
                         alpha=10, beta=8, gamma=3, mu=2, nu=1, eta=1):

    state = np.array(ic, dtype=float)
    v = np.random.rand(3)
    v /= np.linalg.norm(v)

    n_steps = int(t_max / dt)
    lce_sum = 0.0
    t = 0

    # 新增：记录收敛过程的数据
    times = []
    lyap_values = []

    for step in range(n_steps):
        def augmented_system(t, y_aug):
            x, y, z = y_aug[:3]
            dx, dy, dz = scholar_chaos(t, [x, y, z], alpha, beta, gamma, mu, nu, eta)
            J = jacobian(x, y, z, alpha, beta, gamma, mu, nu, eta)
            dv = J @ y_aug[3:]
            return np.concatenate(([dx, dy, dz], dv))

        y_aug = np.concatenate((state, v))
        sol = solve_ivp(augmented_system, [0, dt], y_aug, method='RK45', rtol=1e-8)
        result = sol.y[:, -1]
        state = result[:3]
        v = result[3:]

        norm_v = np.linalg.norm(v)
        v /= norm_v
        lce_sum += np.log(norm_v)
        t += dt

        # 新增：记录每个时间点的指数估计值
        current_lyap = lce_sum / t
        times.append(t)
        lyap_values.append(current_lyap)

    max_lyap = lce_sum / t

    # 新增：绘制收敛曲线
    plt.figure(figsize=(10, 6))
    plt.plot(times, lyap_values, lw=1)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Lyapunov Exponent', fontsize=12)
    plt.title('Convergence of Maximum Lyapunov Exponent', fontsize=14)
    plt.grid(True, alpha=0.5)
    plt.show()

    return max_lyap

initial_condition = [1.0, 1.0, 1.0]
max_lyap = compute_max_lyapunov(initial_condition, t_max=100)
print(f"最大 Lyapunov 指数 ≈ {max_lyap:.5f}")
