import pygame.mouse

from init import *
from World.Lattice import *
from World.load_data import *


class Chose:
    def __init__(self):
        self.tile_list = []
        self.tile_size = 50
        self.chosen_tile = None
        # 地图数据
        self.data = load_data("res/files/map.csv")
        self.map_state = load_data("res/files/map_state")
        self.dirt_img = pygame.image.load('res/imgs/d.png')
        self.grass_img = pygame.image.load('res/imgs/g.png')

        self.races_place = np.full(self.data.shape, '', dtype=object)  # 角色在地图中的位置

        self.race_name = ['长身人', '半身人', '精灵', '矮人', '魔族']
        self.unit_type = ['骑士', '魔法师', '战士', '机关师', '剑士']

        # 角色头像
        self.avatars = [
            pygame.transform.scale(pygame.image.load('res/imgs/characters/1.png'), (self.tile_size, self.tile_size)),
            pygame.transform.scale(pygame.image.load('res/imgs/characters/2.png'), (self.tile_size, self.tile_size)),
            pygame.transform.scale(pygame.image.load('res/imgs/characters/3.png'), (self.tile_size, self.tile_size))
        ]
        self.selected_avatar = None  # 选择的角色

        self.avatar_background_img = pygame.transform.scale(pygame.image.load("res/imgs/detail.png"),
                                                            (WIDTH, self.tile_size + 20))

        # 角色头像框矩形
        self.avatar_rects = []
        avatar_size = 50
        avatar_margin = 10
        for i, avatar in enumerate(self.avatars):
            x = avatar_margin + i * (avatar_size + avatar_margin)
            y = HEIGHT - avatar_size - avatar_margin
            rect = pygame.Rect(x, y, avatar_size, avatar_size)
            self.avatar_rects.append(rect)

    # 选择的角色头像上
    def draw_avatars(self, viewport):
        # 绘制选角背景图
        viewport.blit(self.avatar_background_img, (0, HEIGHT - self.tile_size - 20))

        for i, avatar in enumerate(self.avatars):
            viewport.blit(avatar, self.avatar_rects[i].topleft)
            if self.selected_avatar == i:
                pygame.draw.rect(viewport, (0, 255, 0), self.avatar_rects[i], 1)

    # 点击的角色序号
    def handle_avatar_click(self, pos):
        for i, rect in enumerate(self.avatar_rects):
            if rect.collidepoint(pos):
                self.selected_avatar = i
                break

    def handle_map_click(self, pos):
        col = pos[0] // self.tile_size
        row = pos[1] // self.tile_size
        if 0 <= col < self.data.shape[1] and 0 <= row < self.data.shape[0]:
            if self.selected_avatar is not None:
                self.races_place[row][col] = self.race_name[self.selected_avatar]
                self.map_state[row][col] = self.selected_avatar
                self.selected_avatar = None
            elif self.selected_avatar is None and self.races_place[row][col]:
                self.races_place[row][col] = ''

    # 添加单个图片
    def s_img(self, img, col_count, row_count, map_tile, race):
        img_rect = img.get_rect()
        img_rect.x = col_count * self.tile_size
        img_rect.y = row_count * self.tile_size
        img_tile = (img, img_rect)
        self.tile_list.append(Lattice(img_tile, map_tile, 0, None, race))

    # 指针所处地图瓦片添加边框
    def border(self, pos):
        x, y = pos
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
                    col * self.tile_size,
                    row * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                pygame.draw.rect(viewport, (128, 0, 0), rect, 1)

    def chose_draw(self, viewport):
        self.tile_list = []

        row_count = 0
        for row_data, row_state in zip(self.data, self.map_state):
            col_count = 0
            for data_tile, map_tile in zip(row_data, row_state):
                if self.races_place[row_count][col_count]:
                    img = pygame.transform.scale(self.avatars[map_tile], (self.tile_size, self.tile_size))
                    self.s_img(img, col_count, row_count, map_tile, None)
                elif data_tile == 0:
                    img = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
                    self.s_img(img, col_count, row_count, map_tile, None)
                elif data_tile == 1:
                    img = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
                    self.s_img(img, col_count, row_count, map_tile, None)

                col_count += 1
            row_count += 1

        for tile in self.tile_list:
            tile_x = tile.type[1].x
            tile_y = tile.type[1].y
            viewport.blit(tile.type[0], (tile_x, tile_y))

        if self.chosen_tile is not None:
            # 绘制选中边框
            self.add_border([self.border(self.chosen_tile)], viewport)

        # 鼠标所处位置加边框
        self.add_border([self.border(pygame.mouse.get_pos())], viewport)

        # 绘制角色头像
        self.draw_avatars(viewport)

        return self.races_place
