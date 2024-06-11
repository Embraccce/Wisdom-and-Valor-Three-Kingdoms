class Unit:
    def __init__(self, ID, name, health, magic, attack_power, magic_power, attack_range, physical_def, magic_def, speed,
                 move, jump):
        self.ID = ID  # 单位编号ID
        self.name = name  # 单位名称
        self.health = health  # 生命值
        self.magic = magic  # 魔力值
        self.attack_power = attack_power  # 物理攻击力
        self.magic_power = magic_power  # 魔法攻击力
        self.attack_range = attack_range  # 攻击距离
        self.physical_def = physical_def  # 物理防御
        self.magic_def = magic_def  # 魔法防御
        self.speed = speed  # 动作速度，决定单位行动顺序
        self.move = move  # 移动力，决定单位在地图上的移动能力
        self.jump = jump  # 跳跃力，用于有高度差的地图
        self.action_time = 0  # 行动时间点，用于决定单位何时进行下一个动作
        self.img = "res/imgs/characters/1.png"
        self.death = ["res/imgs/characters/1.png", "res/imgs/characters/2.png", "res/imgs/characters/3.png"]
        self.x = None  # 所在x轴
        self.y = None  # 所在y轴
        self.action = self.speed  # 行动值

    def act(self):
        # 更新单位的行动时间
        self.action_time += 100 / self.speed

    def move_to(self, target):
        # 单位移动的方法，具体逻辑待实现
        pass

    def attack(self, target):
        # 单位进行物理攻击的方法
        damage = max(0, 100*(self.attack_power - target.physical_def))
        target.health -= damage
        return damage

    def in_attack_range(self, target):
        # 检查目标是否在攻击范围内
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        return distance <= self.attack_range

    def cast_spell(self, spell, target):
        # 单位施放魔法的方法，具体逻辑待实现
        pass

    # 计算角色周边的范围
    def calculate_range(self, row, col, range_value, data):
        positions = []
        for i in range(-range_value, range_value + 1):
            for j in range(-range_value, range_value + 1):
                if abs(i) + abs(j) <= range_value:
                    if (0 <= col + j < data.shape[1] and
                            0 <= row + i < data.shape[0] and
                            data[row + i][col + j] != -1):
                        positions.append((row + i, col + j))
        return positions

    def move_border(self, row, col, data):
        return self.calculate_range(row, col, self.move, data)

    def attack_border(self, row, col, data):
        return self.calculate_range(row, col, self.attack_range, data)
