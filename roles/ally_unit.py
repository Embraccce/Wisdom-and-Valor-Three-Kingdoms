from roles.unit import Unit


class AllyUnit(Unit):
    def __init__(self, ID, name, race, unit_type, x, y, health=70):
        super().__init__(ID, name, health, 30, 25, 1, 3, 10, 10, 25, 5, 3)  # 基础设定
        self.race = race  # 种族属性
        self.unit_type = unit_type  # 兵种属性
        self.x = x
        self.y = y
        self.img = "res/imgs/characters/1.png"

        # 根据种族修改属性
        if race == '长身人':
            self.speed += 10
        elif race == '半身人':
            self.speed += 5
            self.attack_power -= 5
            self.jump += 1
        elif race == '精灵':
            self.magic = 50
            self.attack_power = 15
            self.magic_power = 5
            self.attack_range += 2
            self.speed -= 10
            self.move -= 2
            self.jump -= 1
        elif race == '矮人':
            self.health += 20
            self.attack_power -= 5
            self.speed -= 5
            self.move -= 1
            self.jump -= 1
        elif race == '魔族':
            pass  # 如果魔族的属性需要根据关卡来设定，可以在这里进行设定

        # 根据兵种修改属性
        if unit_type == '骑士':
            self.attack_range += 1
            self.jump += 1
            self.attack_power += 5
            self.physical_def -= 2
        elif unit_type == '魔法师':
            self.speed -= 5
            self.move -= 1
            self.jump -= 1
            self.attack_range += 1
            self.magic_def += 5
            self.magic_power += 15
            self.attack_power -= 5
        elif unit_type == '战士':
            self.speed += 5
            self.move += 2
            self.jump -= 1
            self.physical_def += 5
        elif unit_type == '机关师':
            self.speed -= 2
            self.move -= 2
            self.jump += 2
            self.attack_range += 2
            self.magic_power = self.attack_power
            self.physical_def -= 2
        elif unit_type == '剑士':
            self.speed += 2
            self.move += 2
            self.attack_power += 10