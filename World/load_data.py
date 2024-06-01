import numpy as np
import pandas as pd


# 加载数据
def load_data(filename):
    data = np.array(pd.read_csv(filename))
    return data