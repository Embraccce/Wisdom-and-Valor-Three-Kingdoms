import os
import time

import pygame

from init import font_path


class Dialogue:
    def __init__(self, dialogues, width, height):
        self.dialogues = dialogues
        self.index = 0
        self.dialogue_bg = pygame.Surface((width, 150), pygame.SRCALPHA)
        self.dialogue_bg.fill((255, 255, 255, 200))  # 半透明白色背景
        self.font = pygame.font.Font(font_path, 24)
        self.name_font = pygame.font.Font(font_path, 28)
        self.text_color = (73, 43, 13)
        self.width = width
        self.height = height
        self.max_width = width - 40  # 最大宽度，用于换行
        self.shake_offset = 0
        self.last_shake_time = time.time()

        # 获取项目根目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(base_dir)

        self.background_img = pygame.image.load(os.path.join(root_dir, "res", "imgs", "library.png")).convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (width, height))

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

    def draw(self, screen):
        # 绘制整个游戏背景
        screen.blit(self.background_img, (0, 0))

        if self.index < len(self.dialogues):
            screen.blit(self.dialogue_bg, (0, self.height - 150))
            if self.index == 0:
                # 初始的背景介绍文本
                dialogue = self.dialogues[self.index]
                dialogue_lines = self.wrap_text(dialogue, self.font, self.max_width)
                for i, line in enumerate(dialogue_lines):
                    dialogue_surface = self.font.render(line, True, self.text_color)
                    screen.blit(dialogue_surface, (10, self.height - 140 + i * 30))
            else:
                # 其他对话
                character, dialogue = self.dialogues[self.index]
                name_surface = self.name_font.render(character, True, self.text_color)
                screen.blit(name_surface, (10, self.height - 140))

                dialogue_lines = self.wrap_text(dialogue, self.font, self.max_width)
                for i, line in enumerate(dialogue_lines):
                    dialogue_surface = self.font.render(line, True, self.text_color)
                    screen.blit(dialogue_surface, (10, self.height - 100 + i * 30))

            # 绘制提示按Enter的抖动矩形
            if time.time() - self.last_shake_time > 0.1:
                self.shake_offset = 3 * (-1 if self.shake_offset > 0 else 1)
                self.last_shake_time = time.time()

            enter_rect_x = self.width - 100 + self.shake_offset
            enter_rect_y = self.height - 40 + self.shake_offset
            pygame.draw.rect(screen, (128, 128, 128), (enter_rect_x, enter_rect_y, 80, 30))
            enter_text = self.font.render("Enter", True, (255, 255, 255))
            screen.blit(enter_text, (enter_rect_x + 10, enter_rect_y + 5))

    def next(self):
        self.index += 1

    def is_finished(self):
        return self.index >= len(self.dialogues)