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
        self.death = ["res/imgs/characters/1.png", "res/imgs/characters/2.png", "res/imgs/characters/3.png"]
        self.x = None  # 所在x轴
        self.y = None  # 所在y轴
        self.action = self.speed  # 行动值

        self.state = {}  # 状态
        self.skill_cd = [0, 0]

        if name == "莱欧斯":
            self.skills = [{
                'name': '坚韧之盾',
                'target': 'friend',
                'type': 'physical',
                'range': 3,
                'scope': 1,
                'effect1': '无敌',
                'time1': 1,
                'effect2': '',
                'time2': '',
                'multiplier': '',
                'cd': 5,
                'description': '莱欧斯召唤出坚韧的神圣之盾，用以保护自己或盟友免受伤害，持续一回合。'
            },
                {
                    'name': '审判之刃',
                    'target': 'enemy',
                    'type': 'physical',
                    'range': 1,
                    'scope': 1,
                    'effect1': '减速',
                    'time1': 3,
                    'effect2': '',
                    'time2': '',
                    'multiplier': 1.5,
                    'cd': 3,
                    'description': '莱欧斯挥舞审判之剑，对敌人造成巨大的伤害，并施加一定的惩罚效果。'
                }]
        elif name == "玛露希尔":
            self.skills = [
                {
                    'name': '冰封之环',
                    'target': 'enemy',
                    'type': 'magic',
                    'range': 4,
                    'scope': 4,
                    'effect1': '禁锢',
                    'time1': 1,
                    'effect2': '',
                    'time2': '',
                    'multiplier': 0.9,
                    'cd': 5,
                    'description': '玛露希尔施展寒冰魔法，在她周围形成一个冰冻的圆环，对接触到的敌人造成冰冻伤害，并有几率冻结敌人，使其无法移动。'
                },
                {
                    'name': '魔力冲击',
                    'target': 'enemy',
                    'type': 'magic',
                    'range': 3,
                    'scope': 3,
                    'effect1': '',
                    'time1': '',
                    'effect2': '',
                    'time2': '',
                    'multiplier': 1.25,
                    'cd': 4,
                    'description': '玛露希尔聚集体内的所有魔力，进行一次强力的魔力爆发，对周围的敌人造成全方位的魔法伤害。'
                }
            ]
        elif name == "齐尔查克":
            self.skills = [
                {
                    'name': '机关大师',
                    'target': 'enemy',
                    'type': 'magic',
                    'range': 3,
                    'scope': 1,
                    'effect1': '禁锢',
                    'time1': 1,
                    'effect2': '',
                    'time2': '',
                    'multiplier': 1.3,
                    'cd': 4,
                    'description': '齐尔查克擅长操控各种复杂的机关装置。他可以利用工具迅速拆解敌方陷阱，或是操控环境中的机关进行反击，暂时困住或伤害敌人。'
                },
                {
                    'name': '疾速闪避',
                    'target': 'friend',
                    'type': 'physical',
                    'range': 5,
                    'scope': 1,
                    'effect1': '瞬移',
                    'time1': '',
                    'effect2': '瞬移',
                    'time2': 1,
                    'multiplier': '',
                    'cd': 4,
                    'description': '利用半身人灵活的体格和精巧的装置，齐尔查克可以迅速躲避敌人的攻击，瞬间移动到安全的位置。'
                }
            ]
        elif name == "森西":
            self.skills = [
                {
                    'name': '钢铁意志',
                    'target': 'friend',
                    'type': 'physical',
                    'range': 0,
                    'scope': 1,
                    'effect1': '抵抗',
                    'time1': 2,
                    'effect2': '攻击上升',
                    'time2': 1,
                    'multiplier': '',
                    'cd': 3,
                    'description': '森西通过多年的冒险和战斗锻炼出坚韧的意志力。使用此技能时，森西能够暂时免疫所有控制效果，并增强其下回合攻击力。'
                },
                {
                    'name': '暴怒之斧',
                    'target': 'enemy',
                    'type': 'physical',
                    'range': 1,
                    'scope': 1,
                    'effect1': '',
                    'time1': '',
                    'effect2': '',
                    'time2': '',
                    'multiplier': 2,
                    'cd': 4,
                    'description': '森西挥舞着他的巨斧，积攒着内心的愤怒之力，向单个敌人进行一次毁灭性的打击。'
                }
            ]
        elif name == "法琳":
            self.skills = [
                {
                    'name': '自然护佑',
                    'target': 'friend',
                    'type': 'magic',
                    'range': 4,
                    'scope': 1,
                    'effect1': '防御上升',
                    'time1': 3,
                    'effect2': '护盾',
                    'time2': 2,
                    'multiplier': '',
                    'cd': 5,
                    'description': '法琳召唤自然之力，为队友施加一层自然护盾，提升他们的防御力。'
                },
                {
                    'name': '和平之缚',
                    'target': 'enemy',
                    'type': 'magic',
                    'range': 4,
                    'scope': 1,
                    'effect1': '缓慢',
                    'time1': 2,
                    'effect2': '沉默',
                    'time2': 2,
                    'multiplier': '',
                    'cd': 5,
                    'description': '法琳释放和平之力，使敌人陷入和谐的状态，暂时停止攻击并降低其行动能力。'
                }
            ]
        elif name == "娜玛莉":
            self.skills = [
                {
                    'name': '战意风暴',
                    'target': 'friend',
                    'type': 'physical',
                    'range': 0,
                    'scope': 4,
                    'effect1': '攻击上升',
                    'time1': 3,
                    'effect2': '防御上升',
                    'time2': 3,
                    'multiplier': '',
                    'cd': 5,
                    'description': '娜玛莉释放出战意风暴，激励身边的队友，使他们充满战斗力和斗志，大幅度提升全体队友的攻击力和防御力，为团队赢得胜利铺平道路。'
                },
                {
                    'name': '黄金守卫',
                    'target': 'friend',
                    'type': 'physical',
                    'range': 0,
                    'scope': 1,
                    'effect1': '召唤守卫',
                    'time1': 3,
                    'effect2': '',
                    'time2': '',
                    'multiplier': '',
                    'cd': 6,
                    'description': '娜玛莉召唤出一名黄金守卫，为她提供强力支援。'
                }
            ]
        elif name == "菊朗":
            self.skills = [
                {
                    'name': '绝影剑技',
                    'target': 'enemy',
                    'type': 'physical',
                    'range': 3,
                    'scope': 1,
                    'effect1': '瞬移',
                    'time1': '',
                    'effect2': '',
                    'time2': '',
                    'multiplier': 1.25,
                    'cd': 3,
                    'description': '菊朗精通绝影剑技，以无与伦比的速度和灵活性施展剑术，对敌人进行快速而凌厉的攻击。这项技能不仅能迅速击倒敌人，还能在战斗中迅速腾挪，保持战斗的主动性。'
                },
                {
                    'name': '风暴突袭',
                    'target': 'enemy',
                    'type': 'physical',
                    'range': 5,
                    'scope': 1,
                    'effect1': '瞬移',
                    'time1': '',
                    'effect2': '',
                    'time2': '',
                    'multiplier': 1.75,
                    'cd': 5,
                    'description': '菊朗如疾风般突袭敌人，以迅雷不及掩耳之势对目标造成极大伤害。这项技能让他能够在战场上以高速度迅速切入敌方阵型，对目标造成致命打击。'
                }
            ]

    def act(self):
        if 'ice' in self.state and self.state['ice'] > 0:
            self.state['ice'] -= 1
            if self.state['ice'] == 0:
                self.state.pop('ice')
            return False
        elif 'death' in self.state:
            return False
        return True

    def ice(self, num):
        # 一回合不能动
        self.state['ice'] = num

    def move_to(self, target):
        # 单位移动的方法，具体逻辑待实现
        pass

    def attack(self, target, multiplier=1):
        # 单位进行物理攻击的方法
        damage = max(0, self.attack_power - target.physical_def)
        target.health -= 85*multiplier  # damage
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
