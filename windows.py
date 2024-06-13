# coding: utf-8
import pygame
import sys
import pickle
from World.map import *
from pygame.locals import *
from init import *
import textwrap
import threading

clock = pygame.time.Clock()
clock.tick(FPS)

is_home_bgm_playing = False

# 定义一个函数用于播放背景音乐
def play_bgm(bgm_path):
    pygame.mixer.music.load(bgm_path)
    pygame.mixer.music.play(-1)  # -1 表示循环播放

# 定义一个函数用于播放主页背景音乐
def play_home_bgm():
    play_bgm("res/bgm/bgm.mp3")

# 定义一个函数用于播放战斗背景音乐
def play_battle_bgm():
    play_bgm("res/bgm/battle.mp3")

# 在后台线程中播放主页背景音乐
def play_home_bgm_thread():
    global is_home_bgm_playing
    if not is_home_bgm_playing:
        is_home_bgm_playing = True
        play_home_bgm()

# 在后台线程中播放战斗背景音乐
def play_battle_bgm_thread():
    play_battle_bgm()

# 文字动画显示函数
def animate_text(text, pos, font, screen, color=WHITE, delay=0.1):
    x, y = pos
    # 一个个输出文字
    for char in text:
        text_surface = font.render(char, True, color)
        screen.blit(text_surface, (x, y))
        x += text_surface.get_width()
        pygame.display.update()
        # 按键音效
        key_sound.play()
        time.sleep(delay)

# 启动页面类
class StartupScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(art_path, 74)
        self.small_font = pygame.font.Font(art_path, 50)
        self.steps = [
            ("这是一个游戏样本", (WIDTH // 2 - 320, HEIGHT // 2 - 100), self.font),
            ("出品人：游戏开发委员会", (WIDTH // 2 - 300, HEIGHT // 2 + 50), self.small_font)
        ]
        self.current_step = 0

    def show(self):
        self.screen.fill(BLACK)
        for text, pos, font in self.steps:
            animate_text(text, pos, font, self.screen)
            time.sleep(1)  # 显示每段文字后暂停一段时间

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

# 关卡选择界面 废案
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
                    global is_home_bgm_playing
                    is_home_bgm_playing = False
                    battle_bgm_thread = threading.Thread(target=play_battle_bgm_thread)
                    battle_bgm_thread.start()
                    map.run()
                    return
                if return_button.check_click(pygame.mouse.get_pos()):
                    event_manager.post("show_main_page", event_manager)
                    return

# 关卡选择页面类
class LevelSelectPage:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.window_width = WIDTH
        self.window_height = HEIGHT
        self.window_size = (WIDTH, HEIGHT)

        self.width = 200  # 按钮宽度
        self.height = 200  # 按钮高度
        self.gap = 10  # 按钮之间的间隙
        self.columns = 10  # 每行10个按钮
        self.rows = 2  # 总共2行按钮

        # 总共关卡数（这会决定显示多少个关卡！！）
        self.levels = LEVEL

        self.return_button = Button('返回', GREY, 10, 10, size=20)

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("关卡选择")

        self.update_buttons()

        self.dragging = False
        self.offset_x = 0
        self.current_x = 0

    def update_buttons(self):
        self.buttons = []
        for i in range(self.columns * self.rows):
            # 如果有该关卡
            if i <= self.levels - 1:
                button = LibraryButton(f'关卡 {i+1}', PINK, 0, 0, self.width, self.height)
                button.set_image(f'res/imgs/levels/level{i+1}.png')
            # 如果无该关卡
            else :
                button = LibraryButton(f'？？？', PINK, 0, 0, self.width, self.height)
            self.buttons.append(button)

    def handle_events(self, event_manager):
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
                        home_page(event_manager)
                        return
                    # 点击关卡进入关卡详情
                    for i, button in enumerate(self.buttons):
                        # 如果当前存在点击到的关卡，则跳转关卡
                        if button.check_click(event.pos) and i < self.levels:
                            map = GameMap(i + 1, event_manager)
                            # 播放战斗音乐
                            global is_home_bgm_playing
                            is_home_bgm_playing = False
                            battle_bgm_thread = threading.Thread(target=play_battle_bgm_thread)
                            battle_bgm_thread.start()
                            # 进入关卡
                            map.run()
                            return

    def check(self):
        total_width = (len(self.buttons) // self.rows) * (self.width + self.gap)
        self.current_x = min(0, max(-(total_width - self.window_width), self.current_x))

    def render(self):
        # 显示背景图
        screen.blit(choose_bg, (0, 0))
        # 显示返回
        self.return_button.display()
        # 显示关卡选择字体
        title_surface = art_font.render("关卡选择", True, BLACK)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

        # 显示关卡图案
        for i, button in enumerate(self.buttons):
            self.check()
            x = self.current_x + (i // self.rows) * (self.width + self.gap)
            # 关卡y轴
            y = 80 + (i % self.rows) * (self.height + self.gap)
            button.move(x)
            button.rect.y = y
            button.display()

        pygame.display.flip()
        return

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events(self.event_manager)
            self.render()
            clock.tick(60)

# 图鉴详情
class DetailPage:
    def __init__(self, type, id, event_manager):
        self.event_manager = event_manager
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
        self.info = self.get_info_by_id(id)
        self.WHITE = WHITE
        self.return_button = Button('返回', GREY, 10, 10, size=20)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("图鉴详情")

        self.font = pygame.font.Font(art_path, 48)
        self.small_font = pygame.font.Font(font_path, 12)
        if self.type == 3:
            self.small_font = pygame.font.Font(font_path, 24)


    def get_info_by_id(self, id_value):
        # 通过布尔索引查找特定的 id
        return self.character_info[self.character_info['id'] == id_value].iloc[0]

    def render(self):
        # 加载背景图
        screen.blit(library_bg, (0, 0))

        #self.screen.fill(self.WHITE)

        self.return_button.display()
        title_surface = self.font.render(self.info["name"], True, BLACK)
        self.screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 10))

        # 加载图片
        if self.type == 1:
            image_path = f"res/imgs/characters/{self.info['id']}.png"
        elif self.type == 2:
            image_path = f"res/imgs/enemies/{self.info['id']}.png"
        elif self.type == 3:
            image_path = f"res/imgs/weapons/{self.info['id']}.png"
        image = pygame.image.load(image_path)

        image = pygame.transform.scale(image, (300, 300))
        self.screen.blit(image, (50, 80))

        x_offset = 400
        y_offset = 80

        attributes = [key for key in self.info.keys() if key not in ["name", "image", "personality_traits","character_story", "description"]]
        for i in range(0, len(attributes), 2):
            # 针对武器的property进行修改
            attr1 = attributes[i]
            attr2 = attributes[i + 1] if i + 1 < len(attributes) else ""
            attr1_surface = self.small_font.render(f"{attr1}: {self.info[attr1]}", True, BLACK)
            attr2_surface = self.small_font.render(f"{attr2}: {self.info[attr2]}", True, BLACK) if attr2 else None
            
            # 如果是property，就变成对应的属性
            if attr1 == 'property1':
                attr1_surface = self.small_font.render(f"{self.info[attr1]}: {self.info[attr2]}", True, BLACK)
                attr2_surface = self.small_font.render(f"{self.info[attributes[i+2]]}: {self.info[attributes[i+3]]}", True, BLACK)
            if attr1 == 'property2':
                continue

            self.screen.blit(attr1_surface, (x_offset, y_offset))
            if attr2_surface:
                self.screen.blit(attr2_surface, (x_offset + 300, y_offset))
            y_offset += 30

        if self.type != 3:
            # 显示描述信息
            description = self.info.get("personality_traits", "")
            # info_surface = self.small_font.render("人物性格：", True, BLACK)
            # self.screen.blit(info_surface, (x_offset, y_offset))
            # y_offset += 30
            # lines = self.wrap_text(description, self.small_font, 2)  # Adjust the max width as needed
            lines = textwrap.wrap(description, 41)
            for line in lines:
                info_surface = self.small_font.render(line, True, BLACK)
                self.screen.blit(info_surface, (x_offset, y_offset))
                y_offset += 30

            # y_offset += 10

            # 显示人物故事
            story = self.info.get("character_story", "")
            # info_surface = self.small_font.render("人物故事：", True, BLACK)
            # self.screen.blit(info_surface, (x_offset, y_offset))
            # y_offset += 30
            # story_lines = self.wrap_text(story, self.small_font, 2)  # Adjust the max width as needed
            story_lines = textwrap.wrap(story, 41)
            for line in story_lines:
                story_surface = self.small_font.render(line, True, BLACK)
                self.screen.blit(story_surface, (x_offset, y_offset))
                y_offset += 30

        # 显示武器描述
        if self.type == 3:
            y_offset += 30
            story = self.info.get("description", "")
            story_lines = textwrap.wrap(story, 21)
            for line in story_lines:
                story_surface = self.small_font.render(line, True, BLACK)
                self.screen.blit(story_surface, (x_offset, y_offset))
                y_offset += 30

        pygame.display.flip()

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ''
        
        for word in words:
            # Add a space if the current line is not empty
            test_line = current_line + ' ' + word if current_line else word
            # Calculate the width of the test line
            line_width, _ = font.size(test_line)
            if line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.return_button.check_click(event.pos):
                    library_page = LibraryPage(self.character_info, self.event_manager,self.type)
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
        # self.color = color
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
        # pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        
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
    def __init__(self, character_info,  event_manager, type=1):
        self.event_manager = event_manager
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
                info = self.character_info.iloc[i]
                button = LibraryButton(info["name"], PINK, 0, 0, self.width, self.height)
                if self.type == 1:
                    image_path = f"res/imgs/characters/{info['id']}.png"
                elif self.type == 2:
                    image_path = f"res/imgs/enemies/{info['id']}.png"
                elif self.type == 3:
                    image_path = f"res/imgs/weapons/{info['id']}.png"
                button.set_image(image_path)
            else:
                button = LibraryButton('', PINK, 0, 0, self.width, self.height)
            self.buttons.append(button)

    def handle_events(self, event_manager):
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
                        home_page(event_manager)
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
                        for j, button in enumerate(self.buttons):
                            # 这里用text是否等于???来判定是否为空图鉴
                            if button.check_click(event.pos) and button.text:
                                # 进入详情页
                                detail_page = DetailPage(self.type, j + 1, event_manager)
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
            self.handle_events(self.event_manager)
            self.render()
            clock.tick(60)

# 废案：
# 图鉴选择界面（）
def library(event_manager):
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
                    role_page = LibraryPage(character_info, event_manager)
                    role_page.run()
                    return
                if enemy_button.check_click(pygame.mouse.get_pos()):
                    enemy_page = LibraryPage(character_info, event_manager)
                    enemy_page.run()
                    choose_level()
                    return
                if equipment_button.check_click(pygame.mouse.get_pos()):
                    equipment_page = LibraryPage(character_info, event_manager)
                    equipment_page.run()
                    choose_level()
                    return
                if return_button.check_click(pygame.mouse.get_pos()):
                    home_page(event_manager)
                    return

# 主页
def home_page(event_manager):
    # 绘制主页面背景
    screen.blit(bg, (0, 0))

    # 多线程bgm
    # 启动后台线程播放主页背景音乐
    global is_home_bgm_playing
    if not is_home_bgm_playing:
        home_bgm_thread = threading.Thread(target=play_home_bgm_thread)
        home_bgm_thread.start()

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

    def show_home_page(event_manager):
        nonlocal running
        running = False
        # print("Home page shown")
        home_page(event_manager)

    event_manager.subscribe("show_main_page", show_home_page)
############################### 

    # 显示标题
     # 显示关卡选择字体
    title_font = pygame.font.Font(art_path, 80)
    title_surface = title_font.render("这是游戏标题", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 80))

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
                    choose = LevelSelectPage(event_manager)
                    choose.run()
                    return
                if play_button.check_click(pygame.mouse.get_pos()):
                    choose = LevelSelectPage(event_manager)
                    choose.run()
                    return
                if library_button.check_click(pygame.mouse.get_pos()):
                    library = LibraryPage(character_info, event_manager)
                    library.run()
                    return
                if exit_button.check_click(pygame.mouse.get_pos()):
                    # 保存游戏进度
                    with open(saved, "wb") as f:
                        pickle.dump(game_level, f)
                    pygame.quit()
                    raise SystemExit
