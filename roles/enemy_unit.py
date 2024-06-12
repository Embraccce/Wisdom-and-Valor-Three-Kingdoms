from roles.unit import Unit


class EnemyUnit(Unit):
    def __init__(self, ID, name, race, x, y, health=80):
        super().__init__(ID, name, health, 35, 30, 2, 3, 15, 15, 30, 10, 5)  # 基础设定

        self.race = race  # 种族属性
        self.x = x
        self.y = y
        self.img = "res/imgs/six.png"

        # 根据种族修改属性
        if race == '魔族':
            self.speed += 15
        elif race == '妖精':
            self.speed += 5
            self.attack_power -= 2
            self.jump += 1
        elif race == '石巨人':
            self.health += 25
            self.attack_power += 5
            self.speed -= 5
            self.move -= 1
            self.jump -= 1