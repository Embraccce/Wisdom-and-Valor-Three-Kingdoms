# coding: utf-8
import pygame
import sys
import pickle
from pygame.locals import *
from init import*

clock = pygame.time.Clock()
clock.tick(FPS)

# 按键类
class Button(object):
    # 初始化
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, color)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if 'centered_x' in kwargs and kwargs['centered_x']:
            self.x = WIDTH // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'centered_y' in kwargs and kwargs['cenntered_y']:
            self.y = HEIGHT // 2 - self.HEIGHT // 2
        else:
            self.y = y

    # 画图
    def display(self):
        screen.blit(self.surface, (self.x, self.y))

    # 检测是否点击到
    def check_click(self,position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
        if x_match and y_match:
            return True
        else:
            return False

# 图鉴类
class LibraryPage:
    def __init__(self, character_info):
        # 设置窗口尺寸
        self.window_width = WIDTH
        self.window_height = HEIGHT
        self.window_size = (WIDTH, HEIGHT)
        self.character_info = character_info

        # 设置展示格式
        # 图鉴大小
        self.width = 200
        self.height = 300
        # 图鉴间隔(gap为间隔+width)
        self.gap = 100 + self.width

        # 设置颜色
        self.WHITE = (255, 255, 255)
        
        # 返回键
        self.return_button = Button('返回', GREY, 10, 10)

        # 初始化窗口
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("图鉴")

        # 加载图像
        self.character_images = []
        for info in character_info:
            image = pygame.image.load(info["image"]).convert_alpha()
            image = pygame.transform.scale(image,(self.width,self.height))
            self.character_images.append(image)

        # 设置字体
        self.font = font

        # 是否按下左键（拖动）
        self.dragging = False
        # 拖动的偏移量
        self.offset_x = 0
        # 现在的偏移量
        self.current_x = 0

    # 移动图鉴
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    # 滚轮向上滚动，向右滚动10像素
                    self.current_x -= 10
                elif event.button == 5:
                    # 滚轮向下滚动，向左滚动10像素
                    self.current_x += 10
                # 检查是否点击了返回按钮
                if event.button == 1:
                    if self.return_button.check_click(event.pos):
                        library()
                        return


    # 检查图鉴位置，如果拖到最左边或最右边则停止
    def check(self):

        # 图鉴的宽度
        total_width = len(self.character_info) * (self.gap + 1)
        # 检查图鉴位置，确保不会拖动到最左边或最右边
        self.current_x = min(0, max(total_width - self.window_width, self.current_x))

    # 图鉴生成
    def render(self):
        self.screen.fill(self.WHITE)

        # 返回键
        self.return_button.display()
        
        # 画图鉴
        for i, image in enumerate(self.character_images):
            # 检查图鉴偏移量
            self.check()

            # 计算每一张图片的初始x，其中gap为两张图鉴的距离
            x = self.current_x + i * self.gap
            self.screen.blit(image, (x, 50))

            # 显示人物名称
            info = self.character_info[i]
            text_name = info["name"]
            
            # 创建字体对象并绘制名称
            font_name = self.font.render(text_name, True, (0, 0, 0))
            self.screen.blit(font_name, (x + 20, 50 + image.get_height() + 10))

        pygame.display.flip()



    
    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()
            self.render()
            clock.tick(60)
            

# 关卡选择界面
def choose_level():
    # 绘制关卡选择界面图片
    screen.blit(bg, (0,0))

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
                    choose_level()
                    return
                if return_button.check_click(pygame.mouse.get_pos()):
                    home_page()
                    return

# 图鉴界面
def library():
    # 绘制关卡选择界面图片
    screen.blit(bg, (0,0))

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
def home_page():
    # 绘制主页面背景
    screen.blit(bg, (0,0))

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
                    choose_level()
                    return
                if play_button.check_click(pygame.mouse.get_pos()):
                    choose_level()
                    return
                if library_button.check_click(pygame.mouse.get_pos()):
                    library()
                    return
                if exit_button.check_click(pygame.mouse.get_pos()):
                    # 保存游戏进度
                    with open(saved, "wb") as f:
                        pickle.dump(game_level, f)
                    pygame.quit()
                    raise SystemExit