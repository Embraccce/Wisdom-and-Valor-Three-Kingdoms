from roles.unit import Unit


class EnemyUnit(Unit):
    def __init__(self, ID, name, x, y, health=80):
        super().__init__(ID, name, health, 35, 30, 2, 3, 15, 15, 30, 10, 5)  # 基础设定

        self.x = x
        self.y = y
        self.img = "res/imgs/six.png"
