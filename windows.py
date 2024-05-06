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
                if role_button.check_click(pygame.mouse.get_pos()):
                    choose_level()
                    return
                if enemy_button.check_click(pygame.mouse.get_pos()):
                    choose_level()
                    return
                if equipment_button.check_click(pygame.mouse.get_pos()):
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