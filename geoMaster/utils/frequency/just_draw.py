'''
@Project ：DroneContest 
@File    ：just_draw.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/7/1 23:23 
'''

import matplotlib.pyplot as plt
import numpy as np
import io
import base64


def create_random_pic():
    fig, ax = plt.subplots()
    ax.plot(np.random.randn(100))

    return fig,ax
