# coding: utf-8
# 初始化文件
from init import *
from windows import *
from event_manager import EventManager
# 初始化事件管理器
event_manager = EventManager()

# 动态显示页面
startup_screen = StartupScreen(screen)

if __name__ == '__main__': 
    startup_screen.show()
    home_page(event_manager)
