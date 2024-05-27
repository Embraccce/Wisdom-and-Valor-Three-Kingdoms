from unit import Unit


class EnemyUnit(Unit):
    def __init__(self, ID, name, race, unit_type):
        super().__init__(ID, name, 80, 35, 30, 2, 3, 15, 15, 30, 10, 5)  # 基础设定

        self.race = race  # 种族属性
        self.unit_type = unit_type  # 兵种属性

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

        # 根据兵种修改属性
        if unit_type == '魔法师':
            self.attack_range += 3
            self.jump -= 1
            self.attack_power += 7
            self.physical_def -= 3
        elif unit_type == '战士':
            self.speed += 7
            self.move += 3
            self.jump -= 1
            self.physical_def += 7
        elif unit_type == '骑士':
            self.speed -= 3
            self.move -= 1
            self.jump += 1
            self.attack_range += 3
            self.physical_def -= 3

    def attack(self):
        # 实现单位的攻击方法; 可以根据单位的特性进行个性化设计
        pass

    def move(self, direction):
        # 实现单位的移动方法
        pass