from roles.unit import Unit


class AllyUnit(Unit):
    def __init__(self, ID, name, x, y):
        super().__init__(ID, name)  # 基础设定
        super().__init__(ID, name)  # 基础设定
        self.x = x
        self.y = y
