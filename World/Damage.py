import time
import pygame


class DamageText:
    def __init__(self, damage, pos):
        self.damage = str(damage)
        self.pos = pos
        self.start_time = time.time()
        self.font = pygame.font.Font(None, 28)  # 使用默认字体
        self.alpha = 255
        self.duration = 0.7  # 总持续时间
        self.rise_duration = 0.35  # 上升阶段持续时间

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.rise_duration:
            # 上升阶段
            self.pos = (self.pos[0], self.pos[1] - 1)
        else:
            # 下降阶段
            self.pos = (self.pos[0], self.pos[1] + 1)
        self.alpha = max(255 - int(elapsed_time * 255 / self.duration), 0)  # 逐渐消失

    def draw(self, surface):
        if self.alpha > 0:
            text_surface = self.font.render(self.damage, True, (0, 0, 0))
            text_surface.set_alpha(self.alpha)
            surface.blit(text_surface, self.pos)

