import numpy as np
import json


# 加载数据
def load_map_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    data = np.array(data['mapgrid'])
    return data


def load_role_place(shape, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    role_data = data['group1_friends']
    role_place = np.full(shape, '', dtype=object)
    for i in role_data:
        role_place[i['x']][i['y']] = i['name']

    enemy_data = data['group2_enemies']

    enemy_place = np.full(shape, '', dtype=object)
    for j in enemy_data:
        enemy_place[j['x']][j['y']] = j['name']

    return role_place, enemy_place
