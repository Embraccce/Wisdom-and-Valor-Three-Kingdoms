import math

import pygame.mouse
from World.Damage import *
import time
from init import *
from World.Lattice import *
from World.load_data import *
import roles.ally_unit as ally
import roles.enemy_unit as enemy
import time
import os
import shutil
import random


# 按键类（菜单中的按钮）
class Button(object):
    def __init__(self, text, color, x=None, y=None, width=None, size=36, height=None, **kwargs):
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
        screen.blit(self.surface, (
            self.x + (self.width - self.surface.get_width()) // 2,
            self.y + (self.height - self.surface.get_height()) // 2))

    def check_click(self, position):
        x_match = self.x <= position[0] <= self.x + self.width
        y_match = self.y <= position[1] <= self.y + self.height
        return x_match and y_match


# 菜单
class Menu(object):
    def __init__(self, event_manager, gamemap):
        self.continue_Button = Button("继续", WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        self.return_Button = Button("返回主页面", WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        self.active = False
        self.event_manager = event_manager
        self.game_map = gamemap

    def continue_game(self):
        self.active = False

    def return_to_main_page(self):
        self.active = False
        self.event_manager.post("show_main_page", self.event_manager)

    def handle_click(self, position):
        if self.active:
            if self.return_Button.check_click(position):
                self.game_map.save_state()
                self.return_to_main_page()

            elif self.continue_Button.check_click(position):
                self.continue_game()


# 游戏结束显示
class Over(object):
    def __init__(self, event_manager, level, state):
        # 重来按钮
        self.restart_Button = Button("重新来过", WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        # 下一关按钮
        self.next_Button = Button("下一关", WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        # 返回界面按钮
        self.return_Button = Button("返回主页面", WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        self.event_manager = event_manager
        # 当前关卡
        self.level = level
        # state = 1为胜利，= 2为失败
        self.state = state

        # 胜利和失败显示
        if self.state == 1:
            self.title = 'Victory'
        else:
            self.title = 'Lose'

    def restart_game(self):
        map = GameMap(self.level, self.event_manager)
        save_path = 'save/game_state.pkl'

        if os.path.exists(save_path):
            os.remove(save_path)

        map.run()

    def return_to_main_page(self):
        self.event_manager.post("show_main_page", self.event_manager)

    def next(self):
        map = GameMap(self.level + 1, self.event_manager)
        map.run()

    def show(self):
        # 显示胜利或失败
        title_font = pygame.font.Font(art_path, 80)
        title_surface = title_font.render(self.title, True, BLACK)
        screen.blit(title_surface, ((WIDTH // 2) - (title_surface.get_width() // 2), 20))

        # 如果胜利
        if self.state == 1:
            # 如果是最后一关
            if self.level == LEVEL:
                text_surface = art_font.render('恭喜冒险家，您已经走到了世界的尽头', True, BLACK)
                screen.blit(text_surface, (WIDTH // 2 - title_surface.get_width() // 2, 220))
            # 如果不是最后一关
            else:
                self.next_Button.display()
            self.return_Button.display()
        # 如果失败
        else:
            self.restart_Button.display()
            self.return_Button.display()

    def handle_click(self, position):
        # 如果胜利
        if self.state == 1:
            # 如果不是最后一关
            if self.level != LEVEL:
                if self.next_Button.check_click(position):
                    # 下一关
                    return 1
                    # self.next()
        # 如果失败
        else:
            if self.restart_Button.check_click(position):
                return 2
                # self.restart_game()
        # 返回主页
        if self.return_Button.check_click(position):
            return 3
            # self.return_to_main_page()
        return 0


# 战斗地图显示 
class GameMap:
    def __init__(self, level, event_manager):
        # 事件管理器
        self.late_time = 0
        self.type = None
        self.mouse_pressed = False
        self.event_manager = event_manager

        self.screen_width, self.screen_height = WIDTH, HEIGHT  # 窗口大小
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        # 关卡数
        self.level = level

        # 背景云层绘制
        self.cloud_img = pygame.image.load("res/imgs/backgroud.png").convert_alpha()
        self.cloud_img = pygame.transform.scale(self.cloud_img, (self.screen_width, self.screen_height))

        # 创建世界
        self.world = World(level)

        # 创建菜单
        self.menu = Menu(event_manager, self)

        # 创建结束菜单
        self.over = Over(self.event_manager, self.level, 1)
        # 结束标志
        self.flag = 0

        self.dragging = False  # 是否在拖拽地图
        self.start_drag_pos = (0, 0)  # 拖拽位置

        # 是否结束关卡
        self.state = False

        # 角色信息框的位置和尺寸
        # 当前角色（固定在下方的）
        self.fixed_info_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
        # 点击到的角色
        self.selected_info_rect = pygame.Rect(WIDTH - 200, 0, 200, 150)
        self.first_role = None

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
        self.skill_boxes = [pygame.Rect(400, 400, 200, 100), pygame.Rect(620, 400, 200, 100)]

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
            "enemy_place": self.world.enemy_place,
            "Action": self.world.Action
        }
        with open(filename, "wb") as f:
            pickle.dump(state, f)

    # 从文件加载状态
    def load_state(self, filename="save/game_state.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                state = pickle.load(f)
            self.world.races_place = state["races_place"]
            self.world.enemy_place = state["enemy_place"]
            self.world.Action = state["Action"]

    def draw_health_bar(self, character_info, x, y):
        # 计算生命值百分比
        health_percentage = character_info.health / character_info.max_health
        bar_length = int(health_percentage * 196)  # 计算生命条长度, 预留4像素间距

        # 绘制生命条背景
        pygame.draw.rect(self.screen, BLACK, (x, y, 200, 20))

        # 根据健康百分比选择颜色
        if health_percentage > 0.6:
            bar_color = (0, 255, 0)
        elif health_percentage > 0.3:
            bar_color = (255, 165, 0)
        else:
            bar_color = (255, 0, 0)

        # 绘制生命条
        pygame.draw.rect(self.screen, bar_color, (x + 2, y + 2, bar_length, 16))

        # 绘制生命值文本
        font = pygame.font.Font(font_path, 14)
        health_text = f"{character_info.health}/{character_info.max_health}"
        text = font.render(health_text, True, BLACK)
        self.screen.blit(text, (x + 210, y))

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
            if i < len(self.world.Action):
                fixed_character_info = self.world.Action[i]
            else:
                fixed_character_info = None
                break

        # 加载头像
        avatar_path = "res/imgs/characters/1.png"  # 头像路径，可以根据实际情况动态获取
        avatar_img = pygame.image.load(avatar_path).convert_alpha()
        avatar_img = pygame.transform.scale(avatar_img, (50, 50))  # 调整头像大小

        # 绘制头像
        self.screen.blit(avatar_img, (10, HEIGHT - 90))

        # 角色其他信息
        if fixed_character_info:
            info = [
                f"{fixed_character_info.name}", "",
                f"物理攻击: {fixed_character_info.attack_power}",
                f"物理防御: {fixed_character_info.physical_def}",
                f"魔法攻击: {fixed_character_info.magic_power}",
                f"魔法防御: {fixed_character_info.magic_def}"
            ]
        else:
            info = [
                f"咩???", "",
                f"物理攻击: 咩",
                f"物理防御: 咩",
                f"魔法攻击: 咩",
                f"魔法防御: 咩"
            ]

        # 绘制角色信息（每列两个信息）
        for i, line in enumerate(info):
            text = font.render(line, True, BLACK)
            col = i % 2  # 列数
            row = i // 2  # 行数
            x_pos = 70 + col * 200  # 每列宽度为200
            y_pos = HEIGHT - 90 + row * 20
            self.screen.blit(text, (x_pos, y_pos))

        if self.world.current_action != "skill":
            # 绘制按钮
            self.draw_buttons()

        # 绘制生命条
        if fixed_character_info:
            self.draw_health_bar(fixed_character_info, 70, HEIGHT - 30)

    # 鼠标悬浮显示信息框
    def draw_selected_info(self):
        # 创建一个 Surface 对象作为信息框背景
        info_bg = pygame.Surface((200, 100), pygame.SRCALPHA)
        info_bg.fill((128, 128, 128, 128))  # 半透明灰色背景
        self.screen.blit(info_bg, (WIDTH - 200, 0))  # 将半透明背景绘制到屏幕上

        # 字体
        font = pygame.font.Font(font_path, 16)

        if self.world.selected_race:
            race_info = self.world.selected_race  # 当前选中角色的名称
            info = [
                f"名字: {race_info.name}",
                f"种类: 类型",  # 可替换为实际的种类信息
                f"血量： {race_info.health}",  # 可替换为实际的基础信息
                f"魔法： {race_info.magic}"]  # 可替换为实际的基础信息

            for i, line in enumerate(info):
                text = font.render(line, True, BLACK)
                self.screen.blit(text, (WIDTH - 190, 10 + i * 20))

        self.mouse_pressed = False  # 用于跟踪鼠标按钮的状态

        self.type = None

    def wrap_text(self, text, font, max_width):
        lines = []
        current_line = []

        for word in text:
            current_line.append(word)
            if font.size(''.join(current_line))[0] > max_width:
                current_line.pop()
                lines.append(''.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(''.join(current_line))

        return lines

    def draw_skills_info(self):
        info_bg = pygame.Surface((220, 100), pygame.SRCALPHA)
        info_bg.fill((0, 0, 0, 0))  # 半透明灰色背景

        positions = [WIDTH - 620, WIDTH - 380]
        for pos in positions:
            index = positions.index(pos)
            # 绘制圆角矩形
            pygame.draw.rect(info_bg, (128, 128, 128, 128), info_bg.get_rect(), border_radius=15)

            self.screen.blit(info_bg, (pos, HEIGHT - 100))  # 将半透明背景绘制到屏幕上
            font = pygame.font.Font(font_path, 16)

            if self.first_role.skills[index]['time1']:
                info = [f"{self.first_role.skills[index]['name']}"
                        f"     持续回合:{self.first_role.skills[index]['time1']}",
                        f"目标：{self.first_role.skills[index]['target']}        伤害类型:{self.first_role.skills[index]['type']}",
                        f"{self.first_role.skills[index]['description']}"]
            else:
                info = [f"{self.first_role.skills[index]['name']}",
                        f"目标：{self.first_role.skills[index]['target']}        伤害类型:{self.first_role.skills[index]['type']}",
                        f"{self.first_role.skills[index]['description']}"]

            height = HEIGHT - 117
            for i, line in enumerate(info):
                if i == 2:
                    font_dis = pygame.font.Font(font_path, 10)
                    wrapped_lines = self.wrap_text(line, font_dis, 200)
                    for wrapped_line in wrapped_lines:
                        text = font_dis.render(wrapped_line, True, BLACK)
                        height += 20
                        self.screen.blit(text, (pos + 10, height))
                else:
                    if i == 1:
                        text = pygame.font.Font(font_path, 10).render(line, True, BLACK)
                    else:
                        text = font.render(line, True, BLACK)

                    height += 20
                    self.screen.blit(text, (pos + 10, height))

        # 绘制灰色圆形背景
        pygame.draw.circle(self.screen, (128, 128, 128, 128), (WIDTH - 100, HEIGHT - 50), self.button_radius)
        # 绘制按钮文字
        text = pygame.font.Font(font_path, 24).render("返回", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH - 100, HEIGHT - 50))
        self.screen.blit(text, text_rect)

    def skill_button_click(self):
        mouse_pos = pygame.mouse.get_pos()
        distance = ((mouse_pos[0] - (WIDTH - 100)) ** 2 + (mouse_pos[1] - (HEIGHT - 50)) ** 2) ** 0.5

        if distance <= self.button_radius:  # 返回
            self.world.current_action = None
            self.world.selected_border_positions = []
            self.world.draw_border = True
        else:  # 技能
            for i, rect in enumerate(self.skill_boxes):
                skill = [self.first_role.skills[0]['name'], self.first_role.skills[1]['name']]
                x, y = self.first_role.x, self.first_role.y
                if rect.collidepoint(mouse_pos) and i == 0 and not self.first_role.skill_cd[0]:
                    self.world.using_skills(skill[0], x, y, self.first_role.skills[i]['range'])
                if rect.collidepoint(mouse_pos) and i == 1 and not self.first_role.skill_cd[1]:
                    self.world.using_skills(skill[1], x, y, self.first_role.skills[i]['range'])

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
                self.first_role = self.world.Action[0]
                if self.first_role.ID == 1:
                    if button_name == "move" or button_name == "attack":
                        self.world.current_action = button_name
                        self.world.border_positions(self.first_role.x, self.first_role.y, None,
                                                    range_type=self.world.current_action)
                        self.world.add_border(self.world.selected_border_positions, self.screen)
                        self.world.draw_border = True
                        self.late_time = time.time()
                    elif button_name == "skill":
                        self.world.current_action = button_name
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    elif button_name == "end":
                        self.first_role.action = 0
                        self.world.Action_change()

    def events(self):
        for event in pygame.event.get():
            # 如果显示了菜单
            if self.menu.active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.menu.handle_click(pygame.mouse.get_pos())
            # 如果游戏结束
            elif self.state == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.over.handle_click(pygame.mouse.get_pos()) != 0:
                            # 设定结束标识
                            self.flag = self.over.handle_click(pygame.mouse.get_pos())
                            # 退出循环
                            return False
            elif event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.active = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # 左键点击
                    if self.world.current_action == "skill":
                        self.skill_button_click()
                        self.world.check_click(pos)
                        self.late_time = time.time()
                    elif any(button_rect.collidepoint(pos) for button_rect in self.buttons.values()):
                        self.handle_button_click(pos)
                        self.mouse_pressed = True
                        self.late_time = time.time()
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

    def draw_race_avatars(self, ):
        total = 50

        for index, unit in enumerate(self.world.Action):
            # 计算头像的位置
            avatar_y = total

            # 绘制头像
            self.screen.blit(self.races_img[unit.name], (5, avatar_y))

            total += unit.action * 2

    # 按照进度条行动
    def action(self):
        # 绘制带圆角的矩形框
        rect = pygame.Rect(10, 50, 10, HEIGHT - 200)

        # 内部实心圆角矩形
        pygame.draw.rect(self.screen, BLACK, rect, border_radius=5)

        pygame.draw.rect(self.screen, BLACK, rect, width=2, border_radius=5)

        self.draw_race_avatars()

        return

    def find_closest_point(self, points, target):
        x, y = target
        min_distance = float('inf')
        closest_point = None

        for point in points:
            if point:
                xi, yi = point.x, point.y
                distance = math.sqrt((x - xi) ** 2 + (y - yi) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

        return closest_point

    def enemy_act(self):
        if not self.world.Action[0].act():
            self.world.Action_change()
        elif time.time() - self.late_time > 1:
            race = self.world.Action[0]
            pos_enemy = (race.x, race.y)

            # 攻击范围内的人
            races_in_attack = []
            closest_race = None
            for pos in race.attack_border(race.x, race.y, self.world.data):
                race_in_border = self.world.find_race(pos[0], pos[1])
                if race_in_border:
                    if race_in_border.ID == 1:
                        races_in_attack.append(race_in_border)

            # 选择最近的人进行攻击
            if len(races_in_attack):
                target = self.find_closest_point(races_in_attack, pos_enemy)
                if target:
                    size = self.world.tile_size
                    view = self.world.viewport_offset
                    self.world.damage_show(race.attack(target),
                                           ((target.y - 1 / 2) * size - view[0], (target.x - 1 / 2) * size - view[1]))
                    if target.health <= 0:
                        self.world.dying_race.append(target)
            else:
                for ally in self.world.Action:
                    if ally.ID == 1:
                        closest_race = self.find_closest_point([ally, closest_race], pos_enemy)
                if closest_race:
                    print(f'{race.name}打不到别人，想打{closest_race.name}')

                    # 如果攻击范围内没有敌人，寻找最近的敌人并移动到可以攻击的位置
                    potential_positions = race.attack_border(closest_race.x, closest_race.y, self.world.data)
                    potential_positions = [pos for pos in potential_positions if
                                           self.world.find_race(pos[0], pos[1]) is None]

                    # 检查potential_positions中确实可以移动到的位置
                    move_range = set(race.move_border(race.x, race.y, self.world.data))
                    move_positions = list(move_range & set(potential_positions))

                    if move_positions:
                        # 随机移动到可以移动的其中一个位置
                        move_to_pos = random.choice(move_positions)
                        old_x, old_y = race.x, race.y
                        race.x, race.y = move_to_pos[0], move_to_pos[1]
                        self.world.enemy_place[old_x][old_y] = ''
                        self.world.enemy_place[race.x][race.y] = race.name
                        self.world.draw_border = False
                        print(f'{race.name}移动到({race.x}, {race.y})准备攻击{closest_race.name}')
                    else:
                        print(f'{race.name}找不到合适的位置进行攻击')
                        # 结束当前回合
                else:
                    print(f'亖干净了，{race.name}没人打了')

            self.late_time = time.time()
            self.world.Action_change()

    def show_menu(self):
        menu_image_rect = menu.get_rect(center=(WIDTH // 2 + 25, HEIGHT // 2))
        self.screen.blit(menu, menu_image_rect.topleft)

        # 菜单显示
        pos = pygame.mouse.get_pos()
        if self.menu.active:
            if self.menu.return_Button.check_click(pos):
                self.menu.return_Button = Button("返回主页面", RED, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            else:
                self.menu.return_Button = Button("返回主页面", WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            if self.menu.continue_Button.check_click(pos):
                self.menu.continue_Button = Button("继续", RED, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
            else:
                self.menu.continue_Button = Button("继续", WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        self.menu.return_Button.display()
        self.menu.continue_Button.display()

    def draw_info(self):
        # 绘制固定角色信息
        self.draw_fixed_info()
        # 绘制当前选中角色信息
        if self.world.selected_race:
            self.draw_selected_info()

        if self.world.current_action == "skill":
            self.draw_skills_info()

        # 如果菜单激活，则绘制菜单
        if self.menu.active:
            # 创建一个透明的 Surface 作为遮罩
            mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            mask.fill(TRANSPARENT_GRAY)
            self.screen.blit(mask, (0, 0))

            # 绘制菜单图片
            self.show_menu()

    # 如果只剩敌人或己方
    def check_action(self):
        has_ally_unit = any(isinstance(action, ally.AllyUnit) for action in self.world.Action)
        has_enemy_unit = any(isinstance(action, enemy.EnemyUnit) for action in self.world.Action)

        # 如果没有己方角色了
        if not has_ally_unit:
            self.over = Over(self.event_manager, self.level, 2)
            self.over.show()
            # 关卡结束
            self.state = True
        # 如果胜利
        if not has_enemy_unit:
            self.over = Over(self.event_manager, self.level, 1)
            self.over.show()
            # 关卡结束
            self.state = True

    def run(self):
        self.load_state()
        run = True
        while run:
            self.clock.tick(60)
            self.screen.blit(self.cloud_img, (0, 0))
            self.world.draw(self.screen)

            self.draw_info()

            self.action()
            if self.world.Action[0].ID == 2:
                self.enemy_act()

            # 检查关卡是否结束
            self.check_action()

            # 如果结束，则显示结束菜单并等待用户点击
            while self.state:
                # self.screen.blit(self.cloud_img, (0, 0))
                # self.world.draw(self.screen)
                # self.draw_info()
                self.over.show()  # 显示结束菜单
                pygame.display.update()

                # 处理事件并检查是否要退出结束状态
                if not self.events():
                    run = False
                    break

            # 如果没有进入结束状态，处理事件并更新屏幕内容
            if run and not self.state:
                run = self.events()
                pygame.display.update()

                # 处理事件并更新屏幕内容
                run = self.events()
                pygame.display.update()
        # 如果退出循环
        if self.flag == 1:
            self.over.next()
        elif self.flag == 2:
            self.over.restart_game()
        elif self.flag == 3:
            self.over.return_to_main_page()
        pygame.quit()


# 地图信息
class World:
    def __init__(self, level):
        # 地图数据
        self.damage_texts = []
        self.file_path = f'res/files/level{level}.json'
        self.data = load_map_data(self.file_path)
        self.map_state = load_map_data(self.file_path)

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
        self.races_place, self.enemy_place = load_role_place(self.data.shape, self.file_path)
        self.races_img = {}
        self.using_skill = None

        # 行动表
        self.Action = []
        for x in range(self.races_place.shape[0]):
            for y in range(self.races_place.shape[1]):
                if self.races_place[x][y]:
                    self.Action.append(ally.AllyUnit(1, self.races_place[x][y], x=x, y=y))
                elif self.enemy_place[x][y]:
                    self.Action.append(enemy.EnemyUnit(2, self.enemy_place[x][y], x=x, y=y))

        self.selected_race = None
        self.late_time = 0
        self.dying_race = []  # 正在亖的角色
        self.death_animation_index = 0

        # 按照speed属性排序
        self.Action.sort(key=lambda unit: unit.speed)

        self.selected_border_positions = []  # 人物的行动范围
        self.draw_border = False

        # 判断当前是攻击还是移动
        self.current_action = None

    def calcu_cd(self):
        for role in self.Action:
            cd_1, cd_2 = role.skill_cd
            if cd_1 > 0:
                role.skill_cd[0] -= 1
            if cd_2 > 0:
                role.skill_cd[1] -= 1

    def Action_change(self):
        if self.Action[0].ID == 2:
            race = self.Action.pop(0)
            self.Action.append(race)

        if self.Action[0].action <= 0:
            race = self.Action.pop(0)
            race.action = race.speed
            self.Action.append(race)

        self.calcu_cd()

    # 返回该瓦片上的角色
    def find_race(self, row, col):
        for role in self.Action:
            if role.y == col and role.x == row:
                return role

        return None

    def border_positions(self, row, col, skill, range_type='move'):
        if self.find_race(row, col):
            unit = self.find_race(row, col)
            if range_type == 'move':
                self.selected_border_positions = unit.move_border(row, col, self.data)
            elif range_type == 'attack':
                self.selected_border_positions = unit.attack_border(row, col, self.data)
            elif range_type == 'skill':
                self.selected_border_positions = unit.calculate_range(row, col, skill, self.data)
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

    def using_skills(self, skill, x, y, range):
        self.border_positions(x, y, range, range_type=self.current_action)
        self.using_skill = skill
        self.draw_border = True

    def check_health(self, target):
        if target.health <= 0:
            target.state['death'] = 1
            self.dying_race.append(target)

    def check_click(self, pos):
        x, y = pos
        x += self.viewport_offset[0]
        y += self.viewport_offset[1]
        col = x // self.tile_size
        row = y // self.tile_size

        if 0 <= col < self.data.shape[1] and 0 <= row < self.data.shape[0] and self.data[row][col] != -1:
            if self.current_action == 'move' and self.races_place[row][col] == '' and self.enemy_place[row][col] == '':
                if (row, col) in self.selected_border_positions:  # 限制运动范围
                    selected_race_instance = self.Action[0]
                    old_x, old_y = selected_race_instance.x, selected_race_instance.y
                    self.races_place[old_x][old_y] = ''
                    self.races_place[row][col] = selected_race_instance.name

                    selected_race_instance.x = row
                    selected_race_instance.y = col

                    self.draw_border = False
                    # TODO:行动点行动一次减少
                    self.Action[0].action -= 25
                    self.Action_change()

                    self.current_action = None  # 复位当前动作
            elif self.current_action == "attack" and (row, col) in self.selected_border_positions:
                target = self.find_race(row, col)
                if isinstance(target, enemy.EnemyUnit):
                    damage = self.Action[0].attack(target)
                    self.damage_show(damage,
                                     (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - self.tile_size / 2))

                    self.check_health(target)

                    self.draw_border = False
                    self.Action[0].action -= 25
                    self.Action_change()
                    self.current_action = None  # 复位当前动作
                else:
                    print("Invalid target!")
            elif self.current_action == "skill" and (row, col) in self.selected_border_positions:
                target = self.find_race(row, col)
                if isinstance(target, enemy.EnemyUnit):
                    if self.using_skill == '冰封之环':
                        self.damage_show(self.Action[0].attack(target, self.Action[0].skills[0]['multiplier']),
                                         (x, y - self.tile_size / 2))
                        target.ice(1)
                        self.check_health(target)
                    elif self.using_skill == '魔力冲击':
                        self.damage_show(self.Action[0].attack(target, self.Action[0].skills[1]['multiplier']),
                                         (x, y - self.tile_size / 2))
                        self.check_health(target)
                    else:
                        print(f'使用{self.using_skill}')

                    self.Action[0].skill_cd[0] = self.Action[0].skills[0]['cd']
                    self.draw_border = False
                    self.Action[0].action -= 25
                    self.Action_change()
                    self.current_action = None  # 复位当前动作

    def redraw_img(self):
        self.dirt_img_scaled = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
        self.grass_img_scaled = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
        self.detail_img_scaled = pygame.transform.scale(self.detail_img, (self.tile_size, self.tile_size))

        for r in self.Action:
            self.races_img[r.name] = pygame.transform.scale(pygame.image.load(r.img), (self.tile_size, self.tile_size))
        self.tile_size_old = self.tile_size

    # 删除死亡的角色播放动画
    def death_animation(self):
        dying = self.dying_race[-1]
        index = self.Action.index(dying)

        if time.time() - self.late_time > 0.1 and self.death_animation_index + 1 == len(self.Action[index].death):
            x = dying.x
            y = dying.y

            if dying in self.Action:
                if dying.ID == 1:
                    self.races_place[x][y] = ''
                else:
                    self.enemy_place[x][y] = ''
                self.Action.remove(dying)

            self.dying_race.pop(-1)
            self.death_animation_index = 0
            self.late_time = time.time()
            return

        if time.time() - self.late_time > 0.1:
            self.death_animation_index += 1
            self.Action[index].img = self.Action[index].death[self.death_animation_index]
            self.redraw_img()
            self.late_time = time.time()

    def damage_show(self, damage, pos):
        damage_text = DamageText(damage, pos)
        self.damage_texts.append(damage_text)

    def draw(self, viewport):
        if self.dying_race:
            self.death_animation()

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

                if 'ice' in race.state:
                    box = pygame.Surface((self.tile_size, self.tile_size))
                    box.set_alpha(100)
                    box.fill((0, 0, 255))
                    viewport.blit(box, (tile_x, tile_y))
            else:
                viewport.blit(tile.type[0], (tile_x, tile_y))

        mouse_pos = pygame.mouse.get_pos()
        # 鼠标所处位置加边框
        self.add_border([self.border(mouse_pos)], viewport)
        if self.border(mouse_pos) and self.find_race(self.border(mouse_pos)[0], self.border(mouse_pos)[1]):
            self.selected_race = self.find_race(self.border(mouse_pos)[0], self.border(mouse_pos)[1])
        else:
            self.selected_race = None

        if self.draw_border:
            self.add_border(self.selected_border_positions, viewport)

        # 更新和绘制伤害文本
        for damage_text in self.damage_texts:
            damage_text.update()
            damage_text.draw(viewport)

        # 移除已经完全消失的伤害文本
        self.damage_texts = [dt for dt in self.damage_texts if dt.alpha > 0]
