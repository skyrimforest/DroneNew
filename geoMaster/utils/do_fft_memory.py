'''
@Project ：pyfw01 
@File    ：do_fft_memory.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/12/19 13:06 
'''
import datetime
# 内存版本的fft,只需将fft替换为fft_memory模块即可
import os
import re
import time

import numpy as np
from matplotlib import pyplot as plt
from SkyLogger import get_logger

import BaseConfig

logger = get_logger("fft_memory")

last_file_name = None

# 元素均为timestamp:fftdata
fft_data_dict = {

}
# 记录无人机数据timestamp:fftdata
drone_data_dict = {

}

FFT_result = None
Axis_result = None


# 存储到内存中
def save_fft_memory(key:str, value:list):
    global fft_data_dict
    # 记录fft数据 它们已经是按照\n划成行形式
    fft_data_dict[key] = value
    # 维护10个fft数据
    prune_fft_memory()


# 保证内存中只存储10条最新的fft数据
def prune_fft_memory():
    global fft_data_dict
    if len(fft_data_dict) <= 10:
        pass
    else:
        keys = sorted(list(fft_data_dict.keys()))
        for i in range(0, len(keys) - 10):
            del fft_data_dict[keys[i]]


# 存储到内存中
def save_drone_memory(key, value):
    global drone_data_dict
    # 记录drone数据
    drone_data_dict[key] = value
    # 维护10个fft数据
    prune_drone_memory()


# 保证内存中只存储10条最新的fft数据
def prune_drone_memory():
    global drone_data_dict
    if len(drone_data_dict) <= 10:
        pass
    else:
        keys = sorted(list(drone_data_dict.keys()))
        for i in range(0, len(keys) - 10):
            del drone_data_dict[keys[i]]


# 对两个内存变量进行设置
def get_fft_result():
    global FFT_result
    return FFT_result


def get_axis_result():
    global Axis_result
    return Axis_result


def set_fft_result(fft_result):
    global FFT_result
    FFT_result = fft_result


def set_axis_result(axis_result):
    global Axis_result
    Axis_result = axis_result


# FFT原始数据存储到内存中
def do_fft_data_save(recv_data:list, dataName=None):
    # 保证数据存储维持在10条
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") if dataName is None else dataName
    # 存储到内存中 使用时间作为key
    save_fft_memory(current_time, recv_data)
    print(recv_data)
    logger.info("fft data saved to dict")


# 无人机数据存储到内存中
def do_drone_data_save(recv_data, dataName=None):
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") if dataName is None else dataName
    real_data_pre = recv_data.split()
    la_x = 39.912863418590014
    la_y = 116.39701366424
    real_data = f"{real_data_pre[0].decode()} {real_data_pre[-1].decode()} {la_x}_{la_y} {current_time}"
    # 将数据保存到 内存
    save_drone_memory(current_time, real_data)
    logger.info("drone data saved to dict")


# 分割数据并存储到内存中
def get_server_info_and_cut(cli_socket):
    while True:
        # 接收数据
        command = cli_socket.recv(16)
        print(command)
        data_length = int(command.decode().split()[1])
        cnt = 0
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        # recv_data = b""
        recv_data_list=[]
        if data_length > 0:
            while cnt < data_length:
                time.sleep(0.1)
                data = cli_socket.recv(1 * 1024)
                if cnt == 0:
                    info_list = data.split(b'\n')
                    do_drone_data_save(info_list[0], current_time)
                if cnt == data_length - 1:
                    data = data.rstrip()
                # recv_data = recv_data + data
                recv_data_list.append(str(data))
                cnt += 1
            do_fft_data_save(recv_data_list, current_time)
        else:
            logger.info("data very small...")


# 返回最新的时标
def f_find_latest_txt():
    # 找到最新的时标
    global fft_data_dict
    keys = sorted(list(fft_data_dict.keys()), reverse=True)
    # 返回最新的时序
    return keys[0] if len(fft_data_dict) != 0 else None


def f_de_time_stamp(data_i, data_q):
    # 筛除时标、同时提取出来
    x_need_cut = []
    for i in range(len(data_i)):
        if data_i[i] == 20241:
            if data_q[i - 1] < -32769 + 98:
                x_need_cut.append(i)
                data_i[i - 1] = data_i[i]
            else:
                x_need_cut.append(i - 1)
                x_need_cut.append(i)
    for index in sorted(x_need_cut, reverse=True):
        del (data_i[index])
        del (data_q[index])

    time_stamp_idx = [index for index, value in enumerate(data_q) if value < -32768 + 98]
    time_stamp_num = [data_i[i] for i in time_stamp_idx]
    for index in sorted(time_stamp_idx, reverse=True):
        del (data_i[index])
        del (data_q[index])

    for i in range(len(time_stamp_idx)):
        time_stamp_idx[i] = time_stamp_idx[i] - i
    return [data_i, data_q, time_stamp_idx] if [data_i, data_q, time_stamp_idx] else None


def f_readdata(time_stamp):
    global fft_data_dict
    # 以固定格式读数据文件
    data_list_i = []
    data_list_q = []
    v_freq = []
    pattern = r'-?\d+'
    file = fft_data_dict[time_stamp]
    for line in file:
        # 找频点
        print(line)
        num_freq = re.search(r'findin\s*(-?\d+)', line)
        if num_freq:
            v_freq.append(num_freq.group(1))
        num_line = re.findall(r'(-?\d+),(-?\d+)', line)
        # print(num_line)
        # 找数据
        if num_line:
            for match in num_line:
                before_comma, after_comma = map(int, match)
                data_list_i.append(before_comma)
                data_list_q.append(after_comma)
    return [data_list_i, data_list_q, v_freq] if [data_list_i, data_list_q, v_freq] else None


# 从内存中读取数据 并写入到内存中
def f_data2fft_write():
    file_lastest = f_find_latest_txt()  # 自动找最新的时标
    print(file_lastest)
    [data_i, data_q, freq_list] = f_readdata(file_lastest)
    freq = (int(freq_list[0]))  # 读取到的中频
    bandwide = 40e6  # 固定设置的带宽
    # 现在没有心跳包了
    # [data_i, data_q] = f_de_tick(data_i, data_q)
    [data_i, data_q, time_stamp_idx1] = f_de_time_stamp(data_i, data_q)
    data = np.array(data_i) + 1j * np.array(data_q)
    data_fft = np.fft.fftshift(np.fft.fft(data))

    data_fft_a = np.abs(data_fft)
    len_fft = len(data_fft_a)
    freq_axis = np.fft.fftshift(np.fft.fftfreq(len_fft, d=1 / bandwide)) + freq
    # 存储到内存中
    set_fft_result(data_fft_a)
    set_axis_result(freq_axis)


def check_new(new_file):
    global last_file_name
    if new_file == last_file_name:
        return False
    else:
        last_file_name = new_file
        return True


if __name__ == '__main__':
    f = open("1-p.txt", 'r',newline="")
    target_file = []
    for line in f:
        target_file.append(line.rstrip())
    do_fft_data_save(target_file)
    f_data2fft_write()
    print(get_axis_result())
    print(get_fft_result())
    # 绘图
    # plt.figure()
    # plt.plot(get_axis_result(), get_fft_result())
    # plt.show()
