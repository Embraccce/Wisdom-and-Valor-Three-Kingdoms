class Unit:
    def __init__(self, ID, name, health, magic, attack_power, magic_power, attack_range, physical_def, magic_def, speed, move, jump):
        self.ID = ID                      #单位编号ID
        self.name = name                  #单位名称
        self.health = health              #生命值
        self.magic = magic                #魔力值
        self.attack_power = attack_power  #物理攻击力
        self.magic_power = magic_power    #魔法攻击力
        self.attack_range = attack_range  #攻击距离
        self.physical_def = physical_def  #物理防御
        self.magic_def = magic_def        #魔法防御
        self.speed = speed                #动作速度，决定单位行动顺序
        self.move = move                  #移动力，决定单位在地图上的移动能力
        self.jump = jump                  #跳跃力，用于有高度差的地图
        self.action_time = 0              #行动时间点，用于决定单位何时进行下一个动作

    def act(self):
        #更新单位的行动时间
        self.action_time += 100 / self.speed

    def move_to(self, target):
        #单位移动的方法，具体逻辑待实现
        pass

    def attack(self, target):
        #单位进行物理攻击的方法，具体逻辑待实现
        pass

    def cast_spell(self, spell, target):
        #单位施放魔法的方法，具体逻辑待实现
        pass