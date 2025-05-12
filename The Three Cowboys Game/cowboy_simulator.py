import random

class Cowboy:
    def __init__(self, name, hit_rate, priority):
        self.name = name
        self.hit_rate = hit_rate
        self.priority = priority  # 射击优先级列表（如 ["H", "J"]）
        self.alive = True

    def choose_target(self, alive_players):
        # 根据优先级选择存活目标
        for target in self.priority:
            if target in alive_players and target != self.name:
                return target
        return None

    def shoot(self, target):
        if random.random() < self.hit_rate:
            print(f"💥 {self.name} 击中了 {target}！")
            return True
        else:
            print(f"❌ {self.name} 没打中 {target}...")
            return False

def initialize_players():
    return {
        "J": Cowboy("J", 0.8, ["H", "C"]),  # 杰克优先射击约翰
        "H": Cowboy("H", 0.6, ["J", "C"]),  # 约翰优先射击杰克
        "C": Cowboy("C", 0.4, ["J", "H"])   # 卡特优先射击杰克
    }

def get_alive_players(players):
    return [k for k, v in players.items() if v.alive]

def duel_simulation(control_c=False):
    players = initialize_players()
    print("\n===== 决斗开始！ =====")
    print("存活: [J, H, C]")

    while True:
        alive = get_alive_players(players)
        if len(alive) <= 1:
            break

        # 玩家控制卡特的射击
        if "C" in alive and control_c:
            target = input("\n卡特（你）选择射击目标 (J/H): ").upper()
            while target not in ["J", "H"] or not players[target].alive:
                target = input("无效目标，请重新选择 (J/H): ").upper()
        else:
            target = None

        # 自动处理射击逻辑
        deaths = []
        for name in alive:
            player = players[name]
            if not player.alive:
                continue

            # 玩家控制的卡特手动选择目标
            if name == "C" and control_c and target:
                pass  # 已通过输入选择
            else:
                target = player.choose_target(alive)

            if target and players[target].alive:
                print(f"\n{player.name} 正在射击 {target}...")
                if player.shoot(target):
                    deaths.append(target)

        # 更新死亡状态
        for target in set(deaths):
            players[target].alive = False
            print(f"\n⚰️ {target} 被淘汰！")

        # 显示存活状态
        alive = get_alive_players(players)
        print(f"\n存活: {alive if alive else '[全部死亡]'}")

    # 显示结果
    winner = alive[0] if alive else "无人生还"
    print(f"\n===== 胜利者: {winner} =====")
    return winner

# 启动游戏
if __name__ == "__main__":
    while True:  # 新增游戏循环
        print("""
    === 牛仔决斗模拟器 ===
    1. 观看自动模拟
    2. 扮演卡特参与决斗
    q. 退出游戏
        """)
        choice = input("请选择模式 (1/2/q): ").strip()

        if choice == "q":
            print("游戏结束！")
            break

        if choice == "2":
            result = duel_simulation(control_c=True)
        else:
            result = duel_simulation()

        # 新增重启判断
        restart = input("\n是否重新开始游戏？(y/n): ").lower()
        if restart != 'y':
            print("感谢游玩！")
            break
