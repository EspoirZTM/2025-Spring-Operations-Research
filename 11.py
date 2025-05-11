import random
import time
import pygame

# 游戏参数设置
width = 80  # 网格宽度
height = 25  # 网格高度
cell_size = 10  # 每个细胞的尺寸
density = 0.2  # 初始细胞密度
refresh_rate = 0.1  # 刷新间隔（秒）

# 初始化pygame
pygame.init()
screen_width = width * cell_size
screen_height = height * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("康威生命游戏")

def create_initial_grid():
    """创建随机初始网格"""
    return [[1 if random.random() < density else 0
             for _ in range(width)]
            for _ in range(height)]

def count_neighbors(grid, y, x):
    """计算环状拓扑结构中细胞的邻居数量"""
    neighbors = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # 跳过自身
            ny = (y + dy) % height  # 环状拓扑处理
            nx = (x + dx) % width
            neighbors += grid[ny][nx]
    return neighbors

def next_generation(grid):
    """生成下一代细胞状态"""
    new_grid = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            neighbors = count_neighbors(grid, y, x)

            # 应用康威生命游戏规则
            if cell:
                new_grid[y][x] = 1 if 2 <= neighbors <= 3 else 0
            else:
                new_grid[y][x] = 1 if neighbors == 3 else 0
    return new_grid

def display_grid(grid):
    """可视化当前细胞状态"""
    screen.fill((0, 0, 0))  # 用黑色填充背景
    for y in range(height):
        for x in range(width):
            if grid[y][x]:
                pygame.draw.rect(screen, (255, 255, 255), (x * cell_size, y * cell_size, cell_size, cell_size))  # 绘制白色细胞
    pygame.display.flip()

def main():
    """主程序循环"""
    grid = create_initial_grid()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_grid(grid)
        grid = next_generation(grid)
        time.sleep(refresh_rate)

    pygame.quit()

if __name__ == "__main__":
    main()
