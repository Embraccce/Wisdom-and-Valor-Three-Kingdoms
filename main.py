# coding: utf-8
# 初始化文件
from init import *
from windows import *
from event_manager import EventManager
# 初始化事件管理器
event_manager = EventManager()

if __name__ == '__main__': 
    home_page(event_manager)
