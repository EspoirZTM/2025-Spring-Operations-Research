def calculate_alive_at_round_n(N):
    """
    计算并打印第 0 到第 N 轮每个牛仔“在该轮快照时还活着”的概率。
    状态含义：
        A: Jack, John, Carter 都存活
        C: Jack + Carter
        D: John + Carter
        E: 仅 Jack
        F: 仅 John
        G: 仅 Carter
        H: 全灭（无人存活）
    """
    # 初始化第 0 轮的状态概率分布
    current = {
        'A': 1.0,
        'C': 0.0,
        'D': 0.0,
        'E': 0.0,
        'F': 0.0,
        'G': 0.0,
        'H': 0.0
    }

    print("\n轮次 |    Jack   |    John   |   Carter")
    print("----------------------------------------")

    for i in range(N + 1):
        # 快照：统计第 i 轮时“还活着”的概率
        jack_alive   = current['A'] + current['C'] + current['E']
        john_alive   = current['A'] + current['D'] + current['F']
        carter_alive = current['A'] + current['C'] + current['D'] + current['G']

        print(f"{i:>3}  | {jack_alive*100:9.6f}% | {john_alive*100:9.6f}% | {carter_alive*100:9.6f}%")

        # 如果已经是最后一轮，就不用再做转移了
        if i == N:
            break

        # 根据上一轮 current 计算下一轮状态分布
        prev = current.copy()
        current = {
            'A': prev['A'] * 0.048,
            'C': prev['A'] * 0.192 + prev['C'] * 0.12,
            'D': prev['A'] * 0.152 + prev['D'] * 0.24,
            'E': prev['C'] * 0.48   + prev['E'],
            'F': prev['D'] * 0.36   + prev['F'],
            'G': prev['A'] * 0.608 + prev['C'] * 0.08 + prev['D'] * 0.16 + prev['G'],
            'H': prev['C'] * 0.32  + prev['D'] * 0.24 + prev['H']
        }

# 示例：计算并打印前 10 轮各自存活概率快照
if __name__ == "__main__":
    calculate_alive_at_round_n(10)
