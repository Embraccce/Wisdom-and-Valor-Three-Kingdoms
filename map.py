import csv
from init import *


class GameMap:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 400  # 窗口大小
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.cloud_img = pygame.image.load("res/imgs/backgroud.png").convert_alpha()
        self.cloud_img = pygame.transform.scale(self.cloud_img, (self.screen_width, self.screen_height))
        self.world = World()
        self.dragging = False
        self.start_drag_pos = (0, 0)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # you键按下开始拖动地图
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
            # pygame.init()
            # pygame.display.set_caption("MyGame")
            self.clock.tick(60)
            self.screen.blit(self.cloud_img, (0, 0))
            self.world.draw(self.screen)
            run = self.events()
            pygame.display.update()  # 更新屏幕内容
        pygame.quit()


class Lattice:
    def __init__(self, type, state, height, terrain):
        self.type = type
        self.state = state
        self.height = height
        self.terrain = terrain


class World:
    def __init__(self):
        self.tile_size = 20
        # 设置初始视口偏移量
        self.viewport_offset = [0, 0]
        self.tile_list = []
        self.data = self.load_data("res/files/map.csv")
        self.map_state = self.load_data("res/files/map_state")
        self.dirt_img = pygame.image.load('res/imgs/d.png')
        self.grass_img = pygame.image.load('res/imgs/g.png')

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
        self.tile_list = []

        row_count = 0
        for row_data, row_state in zip(self.data, self.map_state):
            col_count = 0
            for data_tile, map_tile in zip(row_data, row_state):
                if data_tile == "0":
                    img = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    data_tile = (img, img_rect)
                    self.tile_list.append(Lattice(data_tile, map_tile, 0, None))
                if data_tile == "1":
                    img = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    data_tile = (img, img_rect)
                    self.tile_list.append(Lattice(data_tile, map_tile, 0, None))
                col_count += 1
            row_count += 1

        for tile in self.tile_list:
            tile_x = tile.type[1].x - self.viewport_offset[0]
            tile_y = tile.type[1].y - self.viewport_offset[1]
            viewport.blit(tile.type[0], (tile_x, tile_y))

    def load_data(self, filename):
        map_data = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map_data.append(list(row))
        return map_data


def R():
    GameMap().run()
# if __name__ == "__main__":
#     GameMap().run()
