import numpy as np

def build_transition_matrix():
    P = np.zeros((7,7))
    # 吸收态自环
    # A  (index 4), B(index 5), C(index 6)
    P[4,4] = 1.0
    P[5,5] = 1.0
    P[6,6] = 1.0

    # 两人对决子链
    # AB 对决 (索引 1 -> 1,4,5)
    pA, pB = 0.8, 0.6
    P[1,1] = (1-pA)*(1-pB)
    P[1,4] = (1-pA)*pB
    P[1,5] = pA*(1-pB)

    # AC 对决 (索引 2 -> 2,4,6)
    pC = 0.4
    P[2,2] = (1-pA)*(1-pC)
    P[2,4] = (1-pA)*pC
    P[2,6] = pA*(1-pC)

    # BC 对决 (索引 3 -> 3,5,6)
    P[3,3] = (1-pB)*(1-pC)
    P[3,5] = (1-pB)*pC
    P[3,6] = pB*(1-pC)

    #三人对决子链
    # ABC (索引 0 -> 0,2,3,6)
    # A瞄准B; B、C瞄准A
    P[0,0] = (1-pB)*(1-pC)*(1-pA)          # 保留 ABC
    P[0,2] = (1-pB)*(1-pC)*pA              # 剩 AC
    P[0,3] = (1 - (1-pB)*(1-pC))*(1-pA)    # 剩 BC
    P[0,6] = 1 - (P[0,0] + P[0,2] + P[0,3]) # 剩 C

    return P

def compute_survival_probs(N_values):
    P = build_transition_matrix()
    v0 = np.zeros(7)
    v0[0] = 1.0  # 初始在状态 ABC

    results = {}
    for N in N_values:
        # 计算 P^N
        PN = np.linalg.matrix_power(P, N)
        vN = v0.dot(PN)
        # 吸收态概率
        pA, pB, pC = vN[4], vN[5], vN[6]
        results[N] = (pA, pB, pC)
    return results

if __name__ == "__main__":
    Ns = [1, 2,3,4,5,6,7,8,9,10,100,1000]
    surv = compute_survival_probs(Ns)

    print("轮数 N | P(A)=Jack存活 | P(B)=John存活 | P(C)=Carter存活")
    print("--------|---------------|---------------|----------------")
    for N in Ns:
        pA, pB, pC = surv[N]
        print(f"{N:>7d} | {pA:13.4f} | {pB:13.4f} | {pC:16.4f}")
