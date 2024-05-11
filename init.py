import pygame
import os
import pickle
# 用来标记只初始化一次
initialized = False

def initialize():
    # 检测是否被初始化过
    global initialized
    if initialized:
        return
    initialized = True

    # 初始化pygame
    pygame.init()
initialize()

# 初始化窗口
HEIGHT = 500
WIDTH = 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (192, 192, 192)
FPS = 60
# 加载宋体字体文件
font_path = "simhei.ttf"  # 这里是你放置宋体字体文件的路径
font = pygame.font.Font(font_path, 36)

# 用户信息
saved = 'usr.pkl'
if not os.path.exists(saved):
    game_level = 0
else:
    with open(saved, 'rb') as f:
        game_level = pickle.load(f)

# 初始化窗口和标题
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('GAME')

# 加载主页背景图
bg = pygame.image.load("image/index.png").convert()
# 改变图像大小
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))

# 加载选择关卡界面背景图
choose_bg = pygame.image.load("image/index.png").convert()
choose_bg = pygame.transform.scale(choose_bg,(WIDTH,HEIGHT))

# 加载图鉴界面背景图
library_bg = pygame.image.load("image/index.png").convert()
library_bg = pygame.transform.scale(library_bg,(WIDTH,HEIGHT))

# 角色信息
role_info = [
    {"name": "勇士", "image": "image/index.png", "attributes": {"HP": 100, "Attack": 50, "Defense": 30}},
    {"name": "法师", "image": "image/index.png", "attributes": {"HP": 80, "Attack": 70, "Defense": 20}},
    {"name": "射手", "image": "image/index.png", "attributes": {"HP": 90, "Attack": 60, "Defense": 25}},
    # 在这里添加更多人物的信息
]