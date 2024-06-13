from roles.unit import Unit


class AllyUnit(Unit):
    def __init__(self, ID, name, x, y, health=70):
        super().__init__(ID, name, health, 30, 25, 1, 3, 10, 10, 25, 5, 3)  # 基础设定
        self.x = x
        self.y = y
        self.img = "res/imgs/characters/1.png"
