import csv
import os
import pygame


# 加载文件数据
def load_data(filename):
    map_data = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map_data.append(list(row))
    return map_data


# 地图格子信息
class Lattice(object):
    def __init__(self, type, state, height, terrain):
        self.type = type  # 格子类型
        self.state = state  # 格子状态
        self.height = height  # 高度
        self.terrain = terrain  # 地形


# 地图
class World(object):
    def __init__(self):
        self.tile_list = []
        self.data = load_data("res/files/map.csv")
        self.map_state = load_data("res/files/map_state")

        # load imgs
        dirt_img = pygame.image.load('res/imgs/d.png')
        grass_img = pygame.image.load('res/imgs/g.png')

        row_count = 0
        for row_data, row_state in zip(self.data, self.map_state):
            col_count = 0
            for data_tile, map_tile in zip(row_data, row_state):
                if data_tile == "0":
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    data_tile = (img, img_rect)
                    self.tile_list.append(Lattice(data_tile, map_tile, 0, None))
                if data_tile == "1":
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    data_tile = (img, img_rect)
                    self.tile_list.append(Lattice(data_tile, map_tile, 0, None))
                col_count += 1
            row_count += 1

    def mov(self, view, x, y):
        if 0 <= view[0] + x <= 400:
            view[0] += x
        elif view[0] + x < 0:
            view[0] = 0
        elif view[0] + x > 400:
            view[0] = 400

        if 0 <= view[1] + y <= 200:
            view[1] += y
        elif view[1] + y < 0:
            view[1] = 0
        elif view[1] + y > 200:
            view[1] = 200
        return view

    def draw(self, viewport):
        for tile in self.tile_list:
            # 调整格子位置以适应视口偏移
            tile_x = tile.type[1].x - viewport_offset[0]
            tile_y = tile.type[1].y - viewport_offset[1]
            # 绘制调整后的格子
            viewport.blit(tile.type[0], (tile_x, tile_y))


pygame.init()
pygame.display.set_caption("MyGame")
tile_size = 50  # 单个格子的大小
screen_width, screen_height = tile_size * 16, tile_size * 8
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()  # 设置时钟

# 加载背景图
cloud_img = pygame.image.load("res/imgs/backgroud.png").convert_alpha()
cloud_img = pygame.transform.scale(cloud_img, (screen_width, screen_height))

# 总体世界
world = World()
button = ['L', 'M', 'R']

# 设置初始视口偏移量
viewport_offset = [0, 0]

run = True
dragging = False  # 添加一个变量来表示是否正在拖动地图
while run:
    clock.tick(120)
    screen.blit(cloud_img, (0, 0))
    world.draw(screen)  # 在视口上绘制地图

    for event in pygame.event.get():  # 循环获取事件
        if event.type == pygame.QUIT:  # 若检测到事件类型为退出，则退出系统
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # 按下you键，开始拖动地图
                dragging = True
                start_drag_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # 松开you键，停止拖动地图
                dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:  # 拖动地图
            new_pos = pygame.mouse.get_pos()
            dx = start_drag_pos[0] - new_pos[0]
            dy = start_drag_pos[1] - new_pos[1]
            start_drag_pos = new_pos

            viewport_offset = world.mov(viewport_offset, dx, dy)

    pygame.display.update()  # 更新屏幕内容

pygame.quit()
