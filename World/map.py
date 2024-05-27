import pandas as pd
import numpy as np
import pygame.mouse

from init import *
import roles.ally_unit as ally


class GameMap:
    def __init__(self):
        self.screen_width, self.screen_height = WIDTH, HEIGHT  # 窗口大小
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        # 背景云层绘制
        self.cloud_img = pygame.image.load("res/imgs/backgroud.png").convert_alpha()
        self.cloud_img = pygame.transform.scale(self.cloud_img, (self.screen_width, self.screen_height))

        # 创建世界
        self.world = World()

        self.dragging = False  # 是否在拖拽地图
        self.start_drag_pos = (0, 0)  # 拖拽位置

        # 角色信息框的位置和尺寸
        # 当前角色（固定在下方的）
        self.fixed_info_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
        # 点击到的角色
        self.selected_info_rect = pygame.Rect(WIDTH - 200, 0, 200, 150)

        # 固定显示的角色信息 TODO：（修改为实际进度条获取）
        self.fixed_character_info = {
            'name': '角色A',
            'level': 'LV.99',
            'atk': 1,
            'def': 1
        }
    # 固定信息框
    def draw_fixed_info(self):
        pygame.draw.rect(self.screen, WHITE, self.fixed_info_rect)
        # 字体
        font = pygame.font.Font(font_path, 16)
        info = [
            "头像",  # 可以替换为角色的图标
            f"名字: {self.fixed_character_info['name']}",
            f"等级: {self.fixed_character_info['level']}",
            f"ATK: {self.fixed_character_info['atk']}",
            f"DEF: {self.fixed_character_info['def']}"
        ]
        for i, line in enumerate(info):
            text = font.render(line, True, BLACK)
            self.screen.blit(text, (10, HEIGHT - 90 + i * 20))
    
    # 点击显示信息框 
    def draw_selected_info(self):
        pygame.draw.rect(self.screen, WHITE, self.selected_info_rect)
        # 字体
        font = pygame.font.Font(font_path, 16)
        if self.world.selected_race:
            race_info = self.world.selected_race[0]  # 当前选中角色的名称
            info = [
                f"名字: {race_info}",
                f"种类: 类型",  # 可替换为实际的种类信息
                "基础信息",  # 可替换为实际的基础信息
            ]
            for i, line in enumerate(info):
                text = font.render(line, True, BLACK)
                self.screen.blit(text, (WIDTH - 190, 10 + i * 20))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    self.world.check_click(pygame.mouse.get_pos())
                elif event.button == 3:  # you键按下开始拖动地图
                    self.dragging = True
                    self.start_drag_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # 滚轮缩放
                    self.world.tile_size += 1
                elif event.button == 5:
                    self.world.tile_size -= 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # you键释放停止拖动地图
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                new_pos = pygame.mouse.get_pos()
                dx = self.start_drag_pos[0] - new_pos[0]
                dy = self.start_drag_pos[1] - new_pos[1]
                self.start_drag_pos = new_pos
                self.world.viewport_offset = self.world.mov(self.world.viewport_offset, dx, dy)

        return True

    def run(self):
        run = True
        while run:
            self.clock.tick(60)
            self.screen.blit(self.cloud_img, (0, 0))
            self.world.draw(self.screen)
            # 绘制固定角色信息
            self.draw_fixed_info()  
            # 绘制当前选中角色信息
            if self.world.selected_race:
                self.draw_selected_info()  
            run = self.events()
            pygame.display.update()  # 更新屏幕内容
        pygame.quit()


# 地图瓦片信息
class Lattice:
    def __init__(self, type, state, height, terrain, race):
        self.type = type  # 瓦片类型
        self.state = state  # 瓦片状态
        self.height = height  # 高度
        self.terrain = terrain  # 忘记是啥了
        self.race = race  # 该瓦片上有无角色


class World:
    def __init__(self):
        # 地图数据
        self.data = self.load_data("res/files/map.csv")
        self.map_state = self.load_data("res/files/map_state")
        self.dirt_img = pygame.image.load('res/imgs/d.png')
        self.grass_img = pygame.image.load('res/imgs/g.png')

        # 瓦片大小
        self.tile_size = 50
        # 设置初始视口偏移量
        self.viewport_offset = [0, 0]
        # 瓦片列表
        self.tile_list = []
        # 地图瓦片上的角色
        self.races_place = np.full(self.data.shape, '', dtype=object)  # 角色在地图中的位置
        self.race = []  # 角色列表

        self.r = pygame.image.load("res/imgs/six.png")
        self.races_place[3][0] = '长身人'
        self.races_place[3][1] = '半身人'
        self.races_place[4][3] = ''

        self.selected_race = None

        self.size = 5
        self.selected_border_positions = []  # 人物的行动范围

    # 返回该瓦片上的角色
    def find_race(self, row, col):
        for tile in self.tile_list:
            if tile.race and row == tile.type[1].y // self.tile_size and col == tile.type[1].x // self.tile_size:
                return tile.race

    def border_positions(self, row, col):
        if self.find_race(row, col):
            self.selected_border_positions = self.find_race(row, col).move_border(row, col, self.data)
        else:
            self.selected_border_positions = []

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

    # 指针所处地图瓦片添加边框
    def border(self, pos):
        x, y = pos
        x += self.viewport_offset[0]
        y += self.viewport_offset[1]
        col = x // self.tile_size
        row = y // self.tile_size

        if 0 <= col < self.data.shape[1] and 0 <= row < self.data.shape[0]:
            if self.data[row][col] != -1:
                return [row, col]

        return None

    def add_border(self, hovered_tiles, viewport):
        # 判读是否加边框
        for hovered_tile in hovered_tiles:
            if hovered_tile:
                row, col = hovered_tile
                rect = pygame.Rect(
                    col * self.tile_size - self.viewport_offset[0],
                    row * self.tile_size - self.viewport_offset[1],
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(viewport, (128, 0, 0), rect, 1)

    # 添加单个图片
    def s_img(self, img, col_count, row_count, map_tile, race):
        img_rect = img.get_rect()
        img_rect.x = col_count * self.tile_size
        img_rect.y = row_count * self.tile_size
        img_tile = (img, img_rect)
        self.tile_list.append(Lattice(img_tile, map_tile, 0, None, race))

    # 转换角色位置
    def check_click(self, pos):
        x, y = pos
        x += self.viewport_offset[0]
        y += self.viewport_offset[1]
        col = x // self.tile_size
        row = y // self.tile_size

        if 0 <= col < self.data.shape[1] and 0 <= row < self.data.shape[0] and self.data[row][col] != -1:
            if self.races_place[row][col] and self.selected_race is None:  # 如果当前位置有角色
                self.selected_race = [self.races_place[row][col], row, col]  # 记录
                self.border_positions(row, col)
            elif self.races_place[row][col] == '' and self.selected_race is not None:  # 点击瓦片没有角色
                if (row, col) in self.selected_border_positions:  # 限制运动范围
                    self.races_place[self.selected_race[1]][self.selected_race[2]] = ''
                    self.races_place[row][col] = self.selected_race[0]
                    self.selected_race[1], self.selected_race[2] = row, col
                    self.selected_race = None
            else:
                self.selected_race = None
                # TODO: 选中一个又点另一个角色？

    def draw(self, viewport):
        self.tile_list = []

        row_count = 0
        for row_data, row_state in zip(self.data, self.map_state):
            col_count = 0
            for data_tile, map_tile in zip(row_data, row_state):
                if self.races_place[row_count][col_count]:  # 确定绘制地点
                    # TODO: id和name的确定方式
                    race = ally.AllyUnit('ID', 'name', self.races_place[row_count][col_count], '骑士')
                else:
                    race = None

                if data_tile == 0:
                    img = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
                    self.s_img(img, col_count, row_count, map_tile, race)
                elif data_tile == 1:
                    img = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
                    self.s_img(img, col_count, row_count, map_tile, race)

                col_count += 1
            row_count += 1

        for tile in self.tile_list:
            tile_x = tile.type[1].x - self.viewport_offset[0]
            tile_y = tile.type[1].y - self.viewport_offset[1]
            viewport.blit(tile.type[0], (tile_x, tile_y))
            if tile.race:
                img = pygame.transform.scale(self.r, (self.tile_size, self.tile_size))
                viewport.blit(img, (tile_x, tile_y))
                if self.selected_race is not None and tile.race.race == self.selected_race[0]:
                    # 绘制选中边框
                    pygame.draw.rect(viewport, (0, 255, 0), (tile_x, tile_y, self.tile_size, self.tile_size), 3)

        # 鼠标所处位置加边框
        self.add_border([self.border(pygame.mouse.get_pos())], viewport)

        if self.selected_race:
            self.add_border(self.selected_border_positions, viewport)

    # 加载数据
    def load_data(self, filename):
        data = np.array(pd.read_csv(filename))
        return data


def R():
    GameMap().run()

