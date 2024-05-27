# coding: utf-8
import pygame
import sys
import pickle
from World.map import *
from pygame.locals import *
from init import *

clock = pygame.time.Clock()
clock.tick(FPS)

# 按键类
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

# 关卡选择界面
def choose_level(event_manager):
    # 绘制关卡选择界面图片
    screen.blit(bg, (0, 0))

    # 绘制关卡选择界面按钮
    play_button = Button('关卡选择', RED, None, 350, centered_x=True)
    return_button = Button('返回', WHITE, None, 400, centered_x=True)

    play_button.display()
    return_button.display()

    while True:
        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button('关卡选择', RED, None, 350, centered_x=True)
        else:
            play_button = Button('关卡选择', WHITE, None, 350, centered_x=True)

        if return_button.check_click(pygame.mouse.get_pos()):
            return_button = Button('返回', RED, None, 400, centered_x=True)
        else:
            return_button = Button('返回', WHITE, None, 400, centered_x=True)

        play_button.display()
        return_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if pygame.mouse.get_pressed()[0]:
                if play_button.check_click(pygame.mouse.get_pos()):
                    map = GameMap(event_manager)
                    map.run()
                    return
                if return_button.check_click(pygame.mouse.get_pos()):
                    event_manager.post("show_main_page")
                    return

# 图鉴详情
class DetailPage:
    def __init__(self, type, id):
        self.window_width = WIDTH
        self.window_height = HEIGHT
        self.window_size = (WIDTH, HEIGHT)
        self.type = type
        self.id = id
        if self.type == 1:
            self.character_info = character_info
        elif self.type == 2:
            self.character_info = enemy_info
        elif self.type == 3:
            self.character_info = weapon_info
        self.info = self.character_info[id]
        self.WHITE = WHITE
        self.return_button = Button('返回', GREY, 10, 10, size=20)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("图鉴详情")
        self.font = pygame.font.Font(font_path, 24)
        self.small_font = pygame.font.Font(font_path, 18)

    def render(self):
        # 加载背景图
        screen.blit(detail_bg, (0, 0))

        #self.screen.fill(self.WHITE)

        self.return_button.display()
        title_surface = self.font.render(self.info["name"], True, BLACK)
        self.screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 10))

        image = pygame.image.load(self.info["image"])
        image = pygame.transform.scale(image, (300, 300))
        self.screen.blit(image, (50, 80))

        x_offset = 400
        y_offset = 80

        attributes = [key for key in self.info.keys() if key not in ["name", "image", "description"]]
        for i in range(0, len(attributes), 2):
            attr1 = attributes[i]
            attr2 = attributes[i + 1] if i + 1 < len(attributes) else ""
            attr1_surface = self.small_font.render(f"{attr1}: {self.info[attr1]}", True, BLACK)
            attr2_surface = self.small_font.render(f"{attr2}: {self.info[attr2]}", True, BLACK) if attr2 else None
            self.screen.blit(attr1_surface, (x_offset, y_offset))
            if attr2_surface:
                self.screen.blit(attr2_surface, (x_offset + 200, y_offset))
            y_offset += 30

        # 显示描述信息
        description = self.info.get("description", "")
        lines = self.wrap_text(description, 50)
        for line in lines:
            info_surface = self.small_font.render(line, True, BLACK)
            self.screen.blit(info_surface, (x_offset, y_offset))
            y_offset += 30

        pygame.display.flip()

    def wrap_text(self, text, width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            if self.small_font.size(current_line + ' ' + word)[0] <= width:
                current_line += (' ' + word if current_line else word)
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.return_button.check_click(event.pos):
                    library_page = LibraryPage(self.character_info, self.type)
                    library_page.run()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.render()
            clock.tick(60)

# 图鉴加载
class LibraryButton:
    def __init__(self, text, color, x, y, width, height):
        # 该角色名字
        self.text = text
        # 框框颜色
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        # 小字体
        self.font = pygame.font.Font(font_path, 18)
        self.image = None

        # 加载框框图片
        self.frame_image = frame
        self.frame_image = pygame.transform.scale(self.frame_image, (width, height))

    # 画图
    def display(self):
        # 绘制灰色矩形
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        
        # 绘制框框图片
        screen.blit(self.frame_image, (self.rect.x, self.rect.y))

        if self.image:
            scaled_image = pygame.transform.smoothscale(self.image, (180, 160))
            screen.blit(scaled_image, (self.rect.x + 10, self.rect.y + 10))
        else:
            # 否则加载默认图片
            scaled_image = pygame.transform.smoothscale(default, (180, 160))
            screen.blit(scaled_image, (self.rect.x + 10, self.rect.y + 10))
        
        # 绘制名字
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery + self.rect.height // 3 + 15))
            screen.blit(text_surface, text_rect)
        else:
            text_surface = self.font.render("？？？", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery + self.rect.height // 3 + 15))
            screen.blit(text_surface, text_rect)

    # 移动位置
    def move(self, x):
        self.rect.x = x

    # 图鉴是否被点击到
    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    # 设置角色图
    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)

# 图鉴类
class LibraryPage:
    def __init__(self, character_info, type=1):
        self.window_width = WIDTH
        self.window_height = HEIGHT
        self.window_size = (WIDTH, HEIGHT)
        # 角色信息
        self.character_info = character_info
        # 类型：角色/敌人还是武器
        self.type = type

        # 图鉴大小
        self.width = 200
        self.height = (HEIGHT - 100) / 2
        self.gap = 10
        # 10列图鉴
        self.columns = 10
        # 2行图鉴
        self.rows = 2

        self.WHITE = WHITE

        self.return_button = Button('返回', GREY, 10, 10, size=20)

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("图鉴")

        self.update_category_buttons()
        self.update_buttons()

        self.dragging = False
        self.offset_x = 0
        self.current_x = 0

    def update_category_buttons(self):
        self.category_buttons = []
        # 是什么类型的图鉴
        if self.type == 1:
            self.category_buttons.append(Button('角色', BLACK, WIDTH // 6 - 100, 40, size=24))
        else:
            self.category_buttons.append(Button('角色', GREY, WIDTH // 6 - 100, 40, size=24))
        if self.type == 2:
            self.category_buttons.append(Button('敌人', BLACK, WIDTH // 4 - 100, 40, size=24))
        else:
            self.category_buttons.append(Button('敌人', GREY, WIDTH // 4 - 100, 40, size=24))
        if self.type == 3:
            self.category_buttons.append(Button('武器', BLACK, 2 * WIDTH // 6 - 100, 40, size=24))
        else:
            self.category_buttons.append(Button('武器', GREY, 2 * WIDTH // 6 - 100, 40, size=24))

    def update_buttons(self):
        self.buttons = []
        for i in range(self.columns * self.rows):
            if i < len(self.character_info):
                info = self.character_info[i]
                button = LibraryButton(info["name"], PINK, 0, 0, self.width, self.height)
                button.set_image(info["image"])
            else:
                button = LibraryButton('', PINK, 0, 0, self.width, self.height)
            self.buttons.append(button)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.current_x -= 10
                elif event.button == 5:
                    self.current_x += 10
                if event.button == 1:
                    if self.return_button.check_click(event.pos):
                        home_page()
                        return
                    # 如果点击到切换图鉴
                    for i, button in enumerate(self.category_buttons):
                        if button.check_click(event.pos):
                            self.current_x = 0
                            self.type = i + 1
                            if self.type == 1:
                                self.character_info = character_info
                            elif self.type == 2:
                                self.character_info = enemy_info
                            elif self.type == 3:
                                self.character_info = weapon_info
                            self.update_category_buttons()
                            self.update_buttons()
                            return
                    # 如果点击到图鉴进入详情
                        for button in self.buttons:
                            # 这里用text是否等于???来判定是否为空图鉴
                            if button.check_click(event.pos) and button.text:
                                # 进入详情页
                                detail_page = DetailPage(self.type, i)
                                detail_page.run()
                                #self.show_details(button.text)
                                return

    def check(self):
        total_width = (len(self.buttons) // self.rows) * (self.width + self.gap)
        self.current_x = min(0, max(-(total_width - self.window_width), self.current_x))

    def render(self):
        screen.blit(library_bg, (0, 0))
        # self.screen.fill(self.WHITE)

        self.return_button.display()
        # 标题设置：图鉴
        title_surface = font.render("万物图鉴", True, BLACK)
        # 标题位置
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 10))

        for button in self.category_buttons:
            button.display()

        for i, button in enumerate(self.buttons):
            self.check()
            x = self.current_x + (i // self.rows) * (self.width + self.gap)
            # 图鉴的y轴
            y = 80 + (i % self.rows) * (self.height + self.gap)
            button.move(x)
            button.rect.y = y
            button.display()

        pygame.display.flip()
        return

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()
            self.render()
            clock.tick(60)

# 废案：
# 图鉴选择界面（）
def library():
    # 绘制关卡选择界面图片
    screen.blit(bg, (0, 0))

    # 绘制图鉴界面按钮
    role_button = Button('角色图鉴', RED, None, 250, centered_x=True)
    enemy_button = Button('敌人图鉴', WHITE, None, 300, centered_x=True)
    equipment_button = Button('装备图鉴', WHITE, None, 350, centered_x=True)
    return_button = Button('返回', WHITE, None, 400, centered_x=True)
    role_button.display()
    enemy_button.display()
    equipment_button.display()
    return_button.display()
    pygame.display.update()

    while True:
        if role_button.check_click(pygame.mouse.get_pos()):
            role_button = Button('角色图鉴', RED, None, 250, centered_x=True)
        else:
            role_button = Button('角色图鉴', WHITE, None, 250, centered_x=True)

        if enemy_button.check_click(pygame.mouse.get_pos()):
            enemy_button = Button('敌人图鉴', RED, None, 300, centered_x=True)
        else:
            enemy_button = Button('敌人图鉴', WHITE, None, 300, centered_x=True)

        if equipment_button.check_click(pygame.mouse.get_pos()):
            equipment_button = Button('装备图鉴', RED, None, 350, centered_x=True)
        else:
            equipment_button = Button('装备图鉴', WHITE, None, 350, centered_x=True)

        if return_button.check_click(pygame.mouse.get_pos()):
            return_button = Button('返回', RED, None, 400, centered_x=True)
        else:
            return_button = Button('返回', WHITE, None, 400, centered_x=True)

        role_button.display()
        enemy_button.display()
        equipment_button.display()
        return_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if pygame.mouse.get_pressed()[0]:
                # 如果点击人物图鉴
                if role_button.check_click(pygame.mouse.get_pos()):
                    role_page = LibraryPage(role_info)
                    role_page.run()
                    return
                if enemy_button.check_click(pygame.mouse.get_pos()):
                    enemy_page = LibraryPage(role_info)
                    enemy_page.run()
                    choose_level()
                    return
                if equipment_button.check_click(pygame.mouse.get_pos()):
                    equipment_page = LibraryPage(role_info)
                    equipment_page.run()
                    choose_level()
                    return
                if return_button.check_click(pygame.mouse.get_pos()):
                    home_page()
                    return

# 主页
def home_page(event_manager):
    # 绘制主页面背景
    screen.blit(bg, (0, 0))

    # 绘制游戏名（主界面上的）
    # game_title = font.render('GAME OF THRONE', True, WHITE)
    # screen.blit(game_title, (WIDTH//2 - game_title.get_WIDTH()//2, 150))

    # 绘制主页面按钮
    continue_button = Button('继续游戏', GREY, None, 250, centered_x=True)
    play_button = Button('开始游戏', WHITE, None, 300, centered_x=True)
    library_button = Button('游戏图鉴', WHITE, None, 350, centered_x=True)
    exit_button = Button('保存并退出', WHITE, None, 400, centered_x=True)

    continue_button.display()
    play_button.display()
    library_button.display()
    exit_button.display()

########## 事件管理器 ##############
    running = True

    def show_home_page():
        nonlocal running
        running = False
        # print("Home page shown")
        home_page(event_manager)

    event_manager.subscribe("show_main_page", show_home_page)
############################### 

    while True:
        if game_level == 0:
            continue_button = Button('继续游戏', GREY, None, 250, centered_x=True)
        elif continue_button.check_click(pygame.mouse.get_pos()):
            continue_button = Button('继续游戏', RED, None, 250, centered_x=True)
        else:
            continue_button = Button('继续游戏', WHITE, None, 250, centered_x=True)

        if play_button.check_click(pygame.mouse.get_pos()):
            play_button = Button('开始游戏', RED, None, 300, centered_x=True)
        else:
            play_button = Button('开始游戏', WHITE, None, 300, centered_x=True)

        if library_button.check_click(pygame.mouse.get_pos()):
            library_button = Button('游戏图鉴', RED, None, 350, centered_x=True)
        else:
            library_button = Button('游戏图鉴', WHITE, None, 350, centered_x=True)

        if exit_button.check_click(pygame.mouse.get_pos()):
            exit_button = Button('保存并退出', RED, None, 400, centered_x=True)
        else:
            exit_button = Button('保存并退出', WHITE, None, 400, centered_x=True)

        continue_button.display()
        play_button.display()
        library_button.display()
        exit_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if pygame.mouse.get_pressed()[0]:
                if game_level > 0 and continue_button.check_click(pygame.mouse.get_pos()):
                    choose_level(event_manager)
                    return
                if play_button.check_click(pygame.mouse.get_pos()):
                    choose_level(event_manager)
                    return
                if library_button.check_click(pygame.mouse.get_pos()):
                    library = LibraryPage(character_info)
                    library.run()
                    return
                if exit_button.check_click(pygame.mouse.get_pos()):
                    # 保存游戏进度
                    with open(saved, "wb") as f:
                        pickle.dump(game_level, f)
                    pygame.quit()
                    raise SystemExit
