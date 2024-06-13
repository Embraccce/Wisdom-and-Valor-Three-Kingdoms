import pygame
import os
import pickle
import pandas as pd
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
BLACK = (0, 0, 0)
PINK = (255, 182, 193)
FPS = 60
TRANSPARENT_GRAY = (128, 128, 128, 128)

# 关卡
LEVEL = 1

# 加载宋体字体文件
font_path = "simhei.ttf"  # 这里是你放置宋体字体文件的路径
font = pygame.font.Font(font_path, 36)
small_font = pygame.font.Font(font_path, 18)

# 加载艺术字体文件
art_path = "art.ttf"
art_font = pygame.font.Font(art_path, 36)
# 用户信息
saved = 'usr.pkl'
if not os.path.exists(saved):
    game_level = 0
else:
    with open(saved, 'rb') as f:
        game_level = pickle.load(f)

# 初始化窗口和标题
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GAME')

# 加载主页背景图
bg = pygame.image.load("res/imgs/index.png").convert()
# 改变图像大小
bg = pygame.transform.scale(bg,(WIDTH, HEIGHT))

# 加载选择关卡界面背景图
choose_bg = pygame.image.load("res/imgs/parchment.png").convert()
choose_bg = pygame.transform.scale(choose_bg,(WIDTH,HEIGHT))

# 加载图鉴界面背景图
library_bg = pygame.image.load("res/imgs/parchment.png").convert()
library_bg = pygame.transform.scale(library_bg,(WIDTH,HEIGHT))

# 加载图鉴默认图片
default = pygame.image.load("res/imgs/default.png")

# 加载框框
frame = pygame.image.load("res/imgs/frame.png")

# 记载图鉴详情背景
detail_bg = pygame.image.load("res/imgs/detail.png").convert()
detail_bg = pygame.transform.scale(detail_bg,(WIDTH,HEIGHT))

# 加载游戏菜单
menu = pygame.image.load("res/imgs/menu.png").convert_alpha()
menu = pygame.transform.scale(menu,(WIDTH/2+100,HEIGHT/2+100))

# 加载音效
# 加载按键音效
key_sound = pygame.mixer.Sound("res/bgm/click.mp3")

# 示例角色信息
# id,name,race,military,gender,personality_traits,character_story,health,magic,attack_power,magic_power,attack_range,physical_def,magic_def,speed,move,jump
character_info = pd.read_csv("data/friendly_characters.csv")

# character_info = [
#     {"name": "角色1", "image": "res/imgs/characters/1.png", "gender": "男", "health": 100, "magic": 80,
#      "physical_attack": 50, "magic_attack": 60, "attack_range": 1.5, "physical_defense": 30, "magic_defense": 40,
#      "action_speed": 1.2, "move_speed": 5, "jump_force": 3, "action_time": "12:00", "description": "角色1的介绍。"},
#     {"name": "角色2", "image": "res/imgs/characters/2.png", "gender": "女", "health": 120, "magic": 70,
#      "physical_attack": 45, "magic_attack": 55, "attack_range": 1.2, "physical_defense": 35, "magic_defense": 45,
#      "action_speed": 1.4, "move_speed": 6, "jump_force": 4, "action_time": "13:00", "description": "角色2的介绍。"},
#     {"name": "角色3", "image": "res/imgs/characters/3.png", "gender": "男", "health": 110, "magic": 90,
#      "physical_attack": 55, "magic_attack": 65, "attack_range": 1.3, "physical_defense": 40, "magic_defense": 50,
#      "action_speed": 1.3, "move_speed": 5.5, "jump_force": 3.5, "action_time": "14:00", "description": "角色3的介绍。"}
# ]

# 示例敌人信息
# id,name,race,military,gender,personality_traits,character_story,health,magic,attack_power,magic_power,attack_range,physical_def,magic_def,speed,move,jump
enemy_info = pd.read_csv("data/enemy_characters.csv")

# enemy_info = [
#     {"name": "敌人1", "image": "res/imgs/characters/1.png", "gender": "男", "health": 100, "magic": 80,
#      "physical_attack": 50, "magic_attack": 60, "attack_range": 1.5, "physical_defense": 30, "magic_defense": 40,
#      "action_speed": 1.2, "move_speed": 5, "jump_force": 3, "action_time": "12:00", "description": "角色1的介绍。"},
#     {"name": "敌人2", "image": "res/imgs/characters/2.png", "gender": "女", "health": 120, "magic": 70,
#      "physical_attack": 45, "magic_attack": 55, "attack_range": 1.2, "physical_defense": 35, "magic_defense": 45,
#      "action_speed": 1.4, "move_speed": 6, "jump_force": 4, "action_time": "13:00", "description": "角色2的介绍。"},
#     {"name": "敌人3", "image": "res/imgs/characters/3.png", "gender": "男", "health": 110, "magic": 90,
#      "physical_attack": 55, "magic_attack": 65, "attack_range": 1.3, "physical_defense": 40, "magic_defense": 50,
#      "action_speed": 1.3, "move_speed": 5.5, "jump_force": 3.5, "action_time": "14:00", "description": "角色3的介绍。"}
# ]


# 示例武器信息
skill_info = pd.read_csv("data/friendly_characters.csv")
buff_info = pd.read_csv("data/friendly_characters.csv")
weapon_info = pd.read_csv("data/equip.csv")

# weapon_info = [
#     {"name": "武器1", "image": "res/imgs/characters/1.png"},
#     {"name": "武器2", "image": "res/imgs/characters/2.png"},
#     {"name": "武器3", "image": "res/imgs/characters/3.png"},
# ]