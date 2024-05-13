import csv
import os
import pygame


# 加载文件数据
def load_data(filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map


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

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile.type[0], tile.type[1])


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

run = True
while run:
    clock.tick(60)
    # screen.blit(bg_img, (0, 0))
    screen.blit(cloud_img, (0, 0))
    world.draw()

    for event in pygame.event.get():  # 循环获取事件
        if event.type == pygame.QUIT:  # 若检测到事件类型为退出，则退出系统
            run = False

        # left, middle, right = pygame.mouse.get_pressed()
        #
        # if left:
        #     print("[MOUSEBUTTONDOWN]:", pygame.mouse.get_pos(), "L")
        # if middle:
        #     print("[MOUSEBUTTONDOWN]:", pygame.mouse.get_pos(), "M")
        # if right:
        #     print("[MOUSEBUTTONDOWN]:", pygame.mouse.get_pos(), "R")
        #
        # if event.type == pygame.MOUSEBUTTONUP:
        #     print("[MOUSEBUTTONUP]:", event.pos, button[event.button - 1])

    pygame.display.update()  # 更新屏幕内容
pygame.quit()
