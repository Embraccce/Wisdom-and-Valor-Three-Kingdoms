import pygame.mouse
import json
from init import *
from World.Lattice import *
from World.load_data import *
import roles.ally_unit as ally
import roles.enemy_unit as enemy


class GameMap:
    def __init__(self, event_manager):
        # 事件管理器
        self.mouse_pressed = False
        self.event_manager = event_manager

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

        # 定义按钮
        self.button_width = 100
        self.button_height = 50
        self.button_radius = 40  # 半径
        self.buttons = {
            "move": pygame.Rect(self.screen_width - self.button_width - 10,
                                self.screen_height - 4 * self.button_height - 20, self.button_width, self.button_height),
            "attack": pygame.Rect(self.screen_width - self.button_width - 10, self.screen_height - 3 *
                                  self.button_height - 15, self.button_width, self.button_height),
            "skill": pygame.Rect(self.screen_width - self.button_width - 10,
                                 self.screen_height - 2 * self.button_height - 10, self.button_width, self.button_height),
            "end": pygame.Rect(self.screen_width - self.button_width - 10,
                               self.screen_height - self.button_height - 5, self.button_width, self.button_height)
        }  #

    def save_state(self, filename="save/game_state.pkl"):
        # 确保保存目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        state = {
            "races_place": self.world.races_place,
            "tile_size": self.world.tile_size,
            "viewport_offset": self.world.viewport_offset,
        }
        with open(filename, "wb") as f:
            pickle.dump(state, f)
        print(f"Game state saved to {filename}")

    # 从文件加载状态
    def load_state(self, filename="save/game_state.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                state = pickle.load(f)
            self.world.races_place = np.array(state["races_place"])
            self.world.tile_size = state["tile_size"]
            self.world.viewport_offset = state["viewport_offset"]
            print(f"Game state loaded from {filename}")
        else:
            print(f"No save file found at {filename}")

    # 固定信息框
    def draw_fixed_info(self):
        pygame.draw.rect(self.screen, WHITE, self.fixed_info_rect)
        
        # 字体
        font = pygame.font.Font(font_path, 16)
        
        # 获取当前固定显示的角色信息
        fixed_character_info = self.world.Action[0]
        
        # 加载头像
        avatar_path = "res/imgs/characters/1.png"  # 头像路径，可以根据实际情况动态获取
        avatar_img = pygame.image.load(avatar_path).convert_alpha()
        avatar_img = pygame.transform.scale(avatar_img, (50, 50))  # 调整头像大小
        
        # 绘制头像
        self.screen.blit(avatar_img, (10, HEIGHT - 90))
        
        # 角色其他信息
        info = [
            f"名字: {fixed_character_info.name}",
            f"种族: {fixed_character_info.race}",
            f"物理攻击: {fixed_character_info.attack_power}",
            f"物理防御: {fixed_character_info.physical_def}",
            f"魔法攻击: {fixed_character_info.magic_power}",
            f"魔法防御: {fixed_character_info.magic_def}"
        ]
        
        # 绘制角色信息（每列两个信息）
        for i, line in enumerate(info):
            text = font.render(line, True, BLACK)
            col = i % 2  # 列数
            row = i // 2  # 行数
            x_pos = 70 + col * 200  # 每列宽度为200
            y_pos = HEIGHT - 90 + row * 20
            self.screen.blit(text, (x_pos, y_pos))

        # 绘制按钮
        self.draw_buttons()

    # 点击显示信息框
    def draw_selected_info(self):
        # 创建一个 Surface 对象作为信息框背景
        info_bg = pygame.Surface((200, 100), pygame.SRCALPHA)
        info_bg.fill((128, 128, 128, 128))  # 半透明灰色背景
        self.screen.blit(info_bg, (WIDTH - 200, 0))  # 将半透明背景绘制到屏幕上

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

        self.mouse_pressed = False  # 用于跟踪鼠标按钮的状态

        self.type = None

    def draw_buttons(self):
        for i, (button_name, button_rect) in enumerate(self.buttons.items()):
            # 按钮之间的间距
            margin = 50

            # 计算每个按钮的位置
            button_x = WIDTH - (len(self.buttons) - i) * (2 * self.button_radius + margin)
            button_y = HEIGHT - self.button_radius - 10

            # 绘制灰色圆形背景
            pygame.draw.circle(self.screen, (128, 128, 128, 128), (button_x, button_y), self.button_radius)

            # 绘制按钮文字
            font = pygame.font.Font(font_path, 24)
            text = font.render(button_name.capitalize(), True, BLACK)
            text_rect = text.get_rect(center=(button_x, button_y))
            self.screen.blit(text, text_rect)

    def handle_button_click(self, pos):
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos) and self.type is None:
                # TODO:怎么进行动作
                if button_name == "move":
                    print("move")
                elif button_name == "attack":
                    print("attack")
                elif button_name == "skill":
                    print("skill")
                elif button_name == "end":
                    print("end")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_manager.post("show_main_page", self.event_manager)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # 左键点击
                    if any(button_rect.collidepoint(pos) for button_rect in self.buttons.values()):
                        self.handle_button_click(pos)
                        self.mouse_pressed = True
                    else:
                        self.world.check_click(pos)
                elif event.button == 3:  # 右键按下开始拖动地图
                    self.dragging = True
                    self.start_drag_pos = pos
                elif event.button == 4:  # 滚轮缩放
                    if self.world.tile_size <= 80:
                        self.world.tile_size += 1
                elif event.button == 5:
                    if self.world.tile_size > 20:
                        self.world.tile_size -= 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False  # 重置鼠标按钮状态
                elif event.button == 3:  # 右键释放停止拖动地图
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                new_pos = pygame.mouse.get_pos()
                dx = self.start_drag_pos[0] - new_pos[0]
                dy = self.start_drag_pos[1] - new_pos[1]
                self.start_drag_pos = new_pos
                self.world.viewport_offset = self.world.mov(self.world.viewport_offset, dx, dy)

        return True

    # 按照进度条行动
    def action(self):
        # TODO: 进度条
    
        return
    def run(self):
        # self.load_state()
        run = True
        while run:
            # print(pygame.mouse.get_pos())
            self.clock.tick(10)
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


class World:
    def __init__(self):
        # 地图数据
        self.data = load_map_data()
        self.map_state = load_map_data()

        # 瓦片大小
        self.tile_size = 50
        self.tile_size_old = 50

        self.dirt_img = pygame.image.load('res/imgs/d.png')
        self.grass_img = pygame.image.load('res/imgs/g.png')
        self.detail_img = pygame.image.load("res/imgs/detail.png")

        # 缓存缩放后的图像
        self.dirt_img_scaled = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
        self.grass_img_scaled = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
        self.detail_img_scaled = pygame.transform.scale(self.detail_img, (self.tile_size, self.tile_size))

        # 设置初始视口偏移量
        self.viewport_offset = [0, 0]
        # 瓦片列表
        self.tile_list = []
        # 地图瓦片上的角色
        self.races_place, self.enemy_place = load_role_place(self.data.shape)
        # print(self.races_place)
        # print(self.enemy_place)

        # 行动表
        self.Action = []
        for x in range(self.races_place.shape[0]):
            for y in range(self.races_place.shape[1]):
                if self.races_place[x][y]:
                    # print(self.races_place[x][y])
                    self.Action.append(ally.AllyUnit(1, self.races_place[x][y], "精灵", "骑士", x, y))
                elif self.enemy_place[x][y]:
                    # print(self.enemy_place[x][y])
                    self.Action.append(enemy.EnemyUnit(1, self.races_place[x][y], "魔族", x, y))

        self.race = []  # 角色列表
        self.selected_race = None
        # 按照speed属性排序
        self.Action.sort(key=lambda unit: unit.speed)


        self.selected_border_positions = []  # 人物的行动范围

    # 返回该瓦片上的角色
    def find_race(self, row, col):
        for tile in self.tile_list:
            if (tile.race is not None and row == ((tile.type[1].y - self.viewport_offset[1]) // self.tile_size) and
                    col == ((tile.type[1].x - self.viewport_offset[0]) // self.tile_size)):
                return tile.race

        return None

    def border_positions(self, row, col):
        if self.find_race(row, col):
            self.selected_border_positions = self.find_race(row, col).move_border(row, col, self.data)
        else:
            self.selected_border_positions = []

    # 窗口移动范围
    def mov(self, view, x, y):
        if -20 <= view[0] + x <= WIDTH + 20:
            view[0] += x
        elif view[0] + x < -20:
            view[0] = -20
        elif view[0] + x > WIDTH + 20:
            view[0] = WIDTH + 20

        if -20 <= view[1] + y <= HEIGHT + 20:
            view[1] += y
        elif view[1] + y < -20:
            view[1] = -20
        elif view[1] + y > HEIGHT + 20:
            view[1] = HEIGHT + 20
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
            if self.find_race(row, col):  # 如果当前位置有角色
                race = self.find_race(row, col)
                if race.ID == 'ally':
                    self.selected_race = [self.races_place[row][col], row, col, race.ID]  # 记录
                else:
                    self.selected_race = [self.enemy_place[row][col], row, col, race.ID]
                self.border_positions(row, col)
            elif (self.races_place[row][col] == '' and self.selected_race is not None
                  and self.enemy_place[row][col] == ''):  # 点击瓦片没有角色
                if self.selected_race[3] == 'ally':
                    if (row, col) in self.selected_border_positions:  # 限制运动范围
                        self.races_place[self.selected_race[1]][self.selected_race[2]] = ''
                        self.races_place[row][col] = self.selected_race[0]
                        self.selected_race[1], self.selected_race[2] = row, col
                        self.selected_race = None
                else:
                    self.selected_race = None
            else:
                self.selected_race = None
                # TODO: 选中一个又点另一个角色？

    def redraw_img(self):
        self.dirt_img_scaled = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
        self.grass_img_scaled = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
        self.detail_img_scaled = pygame.transform.scale(self.detail_img, (self.tile_size, self.tile_size))
        self.tile_size_old = self.tile_size

    def draw(self, viewport):
        self.tile_list = []

        row_count = 0
        for row_data, row_state in zip(self.data, self.map_state):
            col_count = 0
            for data_tile, map_tile in zip(row_data, row_state):
                if self.races_place[row_count][col_count]:  # 确定绘制地点
                    # TODO: id和name的确定方式
                    race = ally.AllyUnit('ally', 'name', self.races_place[row_count][col_count], '骑士', 0 ,0)
                elif self.enemy_place[row_count][col_count]:
                    race = enemy.EnemyUnit('enemy', 'name', self.enemy_place[row_count][col_count], 0, 0)
                    race = ally.AllyUnit('ally', self.races_place[row_count][col_count], 'race', '骑士', 0, 0)
                elif self.enemy_place[row_count][col_count]:
                    race = enemy.EnemyUnit('enemy', self.enemy_place[row_count][col_count], 'race', 0, 0)
                else:
                    race = None

                if self.tile_size_old != self.tile_size:
                    self.redraw_img()

                if data_tile == 1:
                    self.s_img(self.dirt_img_scaled, col_count, row_count, map_tile, race)
                elif data_tile == 2:
                    self.s_img(self.grass_img_scaled, col_count, row_count, map_tile, race)
                elif data_tile == 3:
                    self.s_img(self.detail_img_scaled, col_count, row_count, map_tile, race)

                col_count += 1
            row_count += 1

        for tile in self.tile_list:
            tile_x = tile.type[1].x - self.viewport_offset[0]
            tile_y = tile.type[1].y - self.viewport_offset[1]

            if tile.race:
                # TODO:使用角色自身的图片
                race = self.find_race(tile_y // self.tile_size, tile_x // self.tile_size)
                img = pygame.transform.scale(pygame.image.load(race.img), (self.tile_size, self.tile_size))
                viewport.blit(img, (tile_x, tile_y))
                if self.selected_race is not None and [tile.race.race, tile_y // self.tile_size,
                                                       tile_x // self.tile_size] == self.selected_race:
                    # 绘制选中边框
                    pygame.draw.rect(viewport, (0, 255, 0), (tile_x, tile_y, self.tile_size, self.tile_size), 2)
            else:
                viewport.blit(tile.type[0], (tile_x, tile_y))

        # 鼠标所处位置加边框
        self.add_border([self.border(pygame.mouse.get_pos())], viewport)

        if self.selected_race and self.selected_race[3] == 'ally':
            self.add_border(self.selected_border_positions, viewport)

