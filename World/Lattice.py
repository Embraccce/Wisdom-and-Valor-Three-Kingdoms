# 地图瓦片信息
class Lattice:
    def __init__(self, type, state, height, terrain, race):
        self.type = type  # 瓦片类型
        self.state = state  # 瓦片状态
        self.height = height  # 高度
        self.terrain = terrain  # 忘记是啥了
        self.race = race  # 该瓦片上有无角色
