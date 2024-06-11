import pygame.mouse
import time
from init import *
from World.Lattice import *
from World.load_data import *
import roles.ally_unit as ally
import roles.enemy_unit as enemy

# 按键类（菜单中的按钮）
class Button(object):
    def __init__(self, text, color, x=None, y=None, width=None, size = 36, height=None, **kwargs):
        self.text = text
        self.color = color
        # 字体大小
        self.font = pygame.font.Font(font_path, size)
        self.surface = self.font.render(text, True, color)
        self.width = width if width is not None else self.surface.get_width()
        self.height = height if height is not None else self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = WIDTH // 2 - self.width // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['centered_y']:
            self.y = HEIGHT // 2 - self.height // 2
        else:
            self.y = y

    def display(self):
        screen.blit(self.surface, (self.x + (self.width - self.surface.get_width()) // 2, self.y + (self.height - self.surface.get_height()) // 2))

    def check_click(self, position):
        x_match = self.x <= position[0] <= self.x + self.width
        y_match = self.y <= position[1] <= self.y + self.height
        return x_match and y_match

# 菜单
class Menu(object):
    def __init__(self, event_manager):
        self.continue_Button = Button("继续", WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        self.return_Button = Button("返回主页面", WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        self.active = False
        self.event_manager = event_manager

    def continue_game(self):
        self.active = False

    def return_to_main_page(self):
        self.active = False
        self.event_manager.post("show_main_page", self.event_manager)


    def handle_click(self, position):
        if self.active:
            if self.return_Button.check_click(position):
                self.return_to_main_page()

            elif self.continue_Button.check_click(position):
                self.continue_game()

class GameMap:
    def __init__(self, event_manager):
        # 事件管理器
        self.type = None
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

        # 创建菜单
        self.menu = Menu(event_manager)

        self.dragging = False  # 是否在拖拽地图
        self.start_drag_pos = (0, 0)  # 拖拽位置

        # 角色信息框的位置和尺寸
        # 当前角色（固定在下方的）
        self.fixed_info_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
        # 点击到的角色
        self.selected_info_rect = pygame.Rect(WIDTH - 200, 0, 200, 150)

        # 定义按钮
        self.button_height = HEIGHT - 60
        self.button_radius = 40  # 半径
        self.buttons = {
            "move": pygame.draw.circle(self.screen, (128, 128, 128, 128),
                                       (WIDTH - 4 * 130, self.button_height), self.button_radius),
            "attack": pygame.draw.circle(self.screen, (128, 128, 128, 128),
                                         (WIDTH - 3 * 130, self.button_height), self.button_radius),
            "skill": pygame.draw.circle(self.screen, (128, 128, 128, 128),
                                        (WIDTH - 2 * 130, self.button_height), self.button_radius),
            "end": pygame.draw.circle(self.screen, (128, 128, 128, 128),
                                      (WIDTH - 1 * 130, self.button_height), self.button_radius)
        }

        # 添加按钮抖动
        self.button_shake = {name: 0 for name in self.buttons.keys()}  # 按钮抖动状态

        self.races_img = {}
        for r in self.world.Action:
            self.races_img[r.name] = pygame.transform.scale(pygame.image.load(r.img), (20, 20))

        self.act = False

        # 用于判断当前是attack还是move
        self.current_action = None

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

        i = 0
        # 获取当前固定显示的角色信息
        fixed_character_info = self.world.Action[i]
        while fixed_character_info.ID != 1:
            i += 1
            fixed_character_info = self.world.Action[i]

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
            for character in self.world.Action:
                if self.world.selected_race[1] == character.x and self.world.selected_race[2] == character.y:
                    race = character.race
                    health = character.health
#################################   移动后要修改 TODO    ########################################
            info = [
                f"名字: {race_info}",
                f"种族: {race}",  # 可替换为实际的种类信息
                f"血量：{health}"  # 可替换为实际的基础信息
            ]
            for i, line in enumerate(info):
                text = font.render(line, True, BLACK)
                self.screen.blit(text, (WIDTH - 190, 10 + i * 20))

        self.mouse_pressed = False  # 用于跟踪鼠标按钮的状态

        self.type = None

    def draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        hover = False  # 用于检测是否悬浮在按钮上

        for i, (button_name, button_rect) in enumerate(self.buttons.items()):
            # 按钮之间的间距
            margin = 50

            # 计算每个按钮的位置
            button_x = WIDTH - (len(self.buttons) - i) * (2 * self.button_radius + margin)
            button_y = HEIGHT - self.button_radius - 10

            # 按钮抖动效果
            if self.button_shake[button_name] > 0:
                shake_offset = 5 * (-1) ** self.button_shake[button_name]  # 抖动偏移量
                button_x += shake_offset
                self.button_shake[button_name] -= 1

            # 检查鼠标是否悬浮在按钮上
            if pygame.Rect(button_x - self.button_radius, button_y - self.button_radius, self.button_radius * 2,
                           self.button_radius * 2).collidepoint(mouse_pos):
                hover = True

            # 绘制灰色圆形背景
            pygame.draw.circle(self.screen, (128, 128, 128, 128), (button_x, button_y), self.button_radius)

            # 绘制按钮文字
            font = pygame.font.Font(font_path, 24)
            text = font.render(button_name.capitalize(), True, BLACK)
            text_rect = text.get_rect(center=(button_x, button_y))
            self.screen.blit(text, text_rect)

            # 如果鼠标悬浮在任意按钮上，设置光标为手型，否则恢复默认光标
            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_button_click(self, pos):
        for button_name, button_cir in self.buttons.items():
            if button_cir.collidepoint(pos) and self.type is None:
                # 按钮抖动效果
                self.button_shake[button_name] = 1  # 设置抖动次数

                # TODO:怎么进行动作
                if self.world.Action[0].ID == 1:
                    if button_name == "move" or button_name == "attack":
                        self.world.current_action = button_name
                        self.world.border_positions(self.world.Action[0].x, self.world.Action[0].y,
                                                    range_type=self.world.current_action)
                        self.world.add_border(self.world.selected_border_positions, self.screen)
                        self.world.draw_border = True
                    elif button_name == "skill":
                        self.current_action = None
                    elif button_name == "end":
                        self.current_action = None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.active = True
                    # self.event_manager.post("show_main_page", self.event_manager)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # 左键点击
                    # 传递点击事件给菜单对象处理
                    if self.menu.active:
                        self.menu.handle_click(pygame.mouse.get_pos())
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

        self.world.Action[0]
        self.world.Action.sort(key=lambda unit: unit.speed)
    
        # 绘制带圆角的矩形框
        rect = pygame.Rect(10, 50, 10, HEIGHT - 200)

        # 内部实心圆角矩形
        pygame.draw.rect(self.screen, BLACK, rect, border_radius=5)

        pygame.draw.rect(self.screen, BLACK, rect, width=2, border_radius=5)

        self.draw_race_avatars(5, 50, 20)
        
        return 

    def enemy_act(self):
        self.world.Action_change()

    def draw_race_avatars(self, x, y, width):
        total = y
        for index, unit in enumerate(self.world.Action):
            # 计算头像的位置
            avatar_x = x
            avatar_y = (total + unit.speed) / 2  # y + index * (avatar_size + padding) +
            total += avatar_y

            # 绘制头像
            self.screen.blit(self.races_img[unit.name], (avatar_x, avatar_y))

    def run(self):
        # self.load_state()
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

            self.action()
            if self.world.Action[0].ID == 2:
                self.enemy_act()
            
            # 如果菜单激活，则绘制菜单
            if self.menu.active:
                # 创建一个透明的 Surface 作为遮罩
                mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                mask.fill(TRANSPARENT_GRAY)
                self.screen.blit(mask, (0, 0))
                
                # 绘制菜单图片
                menu_image_rect = menu.get_rect(center=(WIDTH // 2 + 25, HEIGHT // 2))
                self.screen.blit(menu, menu_image_rect.topleft)

                self.menu.return_Button.display()
                self.menu.continue_Button.display()

            # 处理事件并更新屏幕内容
            run = self.events()
            pygame.display.update()
        pygame.quit()


class World:
    def __init__(self):
        # 地图数据
        self.data = load_map_data()
        self.map_state = load_map_data()

        # 瓦片大小
        self.tile_size = 50
        self.tile_size_old = 0

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
        self.races_img = {}

        # 行动表
        self.Action = []
        for x in range(self.races_place.shape[0]):
            for y in range(self.races_place.shape[1]):
                if self.races_place[x][y]:
                    self.Action.append(ally.AllyUnit(1, self.races_place[x][y], "精灵", "骑士", x, y))
                elif self.enemy_place[x][y]:
                    self.Action.append(enemy.EnemyUnit(2, self.races_place[x][y], "魔族", x, y))

        self.selected_race = None
        # 按照speed属性排序
        self.Action.sort(key=lambda unit: unit.speed)

        self.selected_border_positions = []  # 人物的行动范围
        self.draw_border = False

        # 判断当前是攻击还是移动
        self.current_action = None

    def Action_change(self):
        race = self.Action.pop(0)
        self.Action.append(race)

    # 返回该瓦片上的角色
    def find_race(self, row, col):
        for role in self.Action:
            if role.y == col and role.x == row:
                return role

        return None

    def border_positions(self, row, col, range_type='move'):
        if self.find_race(row, col):
            unit = self.find_race(row, col)
            if range_type == 'move':
                self.selected_border_positions = unit.move_border(row, col, self.data)
            elif range_type == 'attack':
                self.selected_border_positions = unit.attack_border(row, col, self.data)
        else:
            self.selected_border_positions = []

    # 窗口移动范围
    def mov(self, view, x, y):
        if -40 <= view[0] + x <= WIDTH + 40:
            view[0] += x
        elif view[0] + x < -40:
            view[0] = -40
        elif view[0] + x > WIDTH + 40:
            view[0] = WIDTH + 40

        if -40 <= view[1] + y <= HEIGHT + 40:
            view[1] += y
        elif view[1] + y < -40:
            view[1] = -40
        elif view[1] + y > HEIGHT + 40:
            view[1] = HEIGHT + 40
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
        # 判断是否加边框
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

    # 删除死亡的角色
    def dele_death_race(self, target):
        x = target.x
        y = target.y
        if target in self.Action:
            if target.ID == 1:
                self.races_place[x][y] = ''
            else:
                self.enemy_place[x][y] = ''
            self.Action.remove(target)

    def check_click(self, pos):
        x, y = pos
        x += self.viewport_offset[0]
        y += self.viewport_offset[1]
        col = x // self.tile_size
        row = y // self.tile_size

        if 0 <= col < self.data.shape[1] and 0 <= row < self.data.shape[0] and self.data[row][col] != -1:
            race = self.find_race(row, col)
            if self.current_action not in ["move", "attack"] and race:  # 如果当前操作不是移动or攻击，并且当前位置有角色
                if race.ID == 1:
                    self.selected_race = [self.races_place[row][col], row, col, race.ID]  # 记录
                else:
                    self.selected_race = [self.enemy_place[row][col], row, col, race.ID]

            if self.current_action == 'move' and self.races_place[row][col] == '' and self.enemy_place[row][col] == '':  # 点击瓦片没有角色
                if (row, col) in self.selected_border_positions:  # 限制运动范围
                    selected_race_instance = self.Action[0]
                    old_x, old_y = selected_race_instance.x, selected_race_instance.y
                    self.races_place[old_x][old_y] = ''
                    self.races_place[row][col] = selected_race_instance.name

                    selected_race_instance.x = row
                    selected_race_instance.y = col

                    self.draw_border = False
                    self.Action_change()
                    self.current_action = None  # 复位当前动作

            if self.current_action == "attack" and (row, col) in self.selected_border_positions:
                target = self.find_race(row, col)
                if isinstance(target, enemy.EnemyUnit):
                    damage = self.Action[0].attack(target)
                    print(f"Attacked {target.ID} for {damage} damage")

                    if target.health <= 0:
                        self.dele_death_race(target)
                        print("target out")
                    self.draw_border = False
                    self.Action_change()
                    self.current_action = None  # 复位当前动作
                else:
                    print("Invalid target!")

    def redraw_img(self):
        self.dirt_img_scaled = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
        self.grass_img_scaled = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
        self.detail_img_scaled = pygame.transform.scale(self.detail_img, (self.tile_size, self.tile_size))

        for r in self.Action:
            self.races_img[r.name] = pygame.transform.scale(pygame.image.load(r.img), (self.tile_size, self.tile_size))
        self.tile_size_old = self.tile_size

    def draw(self, viewport):
        self.tile_list = []

        if self.tile_size_old != self.tile_size:
            self.redraw_img()

        row_count = 0
        for row_data, row_state in zip(self.data, self.map_state):
            col_count = 0
            for data_tile, map_tile in zip(row_data, row_state):
                if self.races_place[row_count][col_count]:  # 确定绘制地点
                    race = 1
                elif self.enemy_place[row_count][col_count]:
                    race = 2
                else:
                    race = None

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
                race = self.find_race(tile.type[1].y // self.tile_size, tile.type[1].x // self.tile_size)
                viewport.blit(self.races_img[race.name], (tile_x, tile_y))
                if self.selected_race is not None and [race.name, tile_y // self.tile_size,
                                                       tile_x // self.tile_size] == self.selected_race:
                    # 绘制选中边框
                    pygame.draw.rect(viewport, (0, 255, 0), (tile_x, tile_y, self.tile_size, self.tile_size), 2)
            else:
                viewport.blit(tile.type[0], (tile_x, tile_y))

        # 鼠标所处位置加边框
        self.add_border([self.border(pygame.mouse.get_pos())], viewport)

        if self.draw_border:
            self.add_border(self.selected_border_positions, viewport)
