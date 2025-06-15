'''
@Project ：pyfw01 
@File    ：do_fft.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/9/3 19:22 
'''
import os
import re

import numpy as np
from matplotlib import pyplot as plt
from SkyLogger import get_logger

import BaseConfig

logger = get_logger("fft")

last_file_name=None

def f_find_latest_txt(folder_path):
    # 找到最新的文件名
    # 存储文件名和最后修改时间的元组列表
    files_with_times = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            # 获取文件的完整路径
            file_path = os.path.join(folder_path, filename)
            # 获取文件的最后修改时间
            modification_time = os.path.getmtime(file_path)
            # 将文件名和修改时间添加到列表中
            files_with_times.append((filename, modification_time))

    # 按修改时间对文件进行排序，最新的文件时间戳最大
    files_with_times.sort(key=lambda x: x[1])

    # 最新的n个文件保留,剩下的丢掉
    file_to_remove_number = len(files_with_times) - BaseConfig.RESERVED_FILE_NUMBER
    if file_to_remove_number > 0:
        logger.info("older files removed...")
        file_to_remove_list = files_with_times[:file_to_remove_number]
        for item in file_to_remove_list:
            os.remove(os.path.join(folder_path, item[0]))
    # 返回最新的.txt文件名
    return files_with_times[-1][0] if files_with_times else None


def f_de_tick(data_i, data_q):
    # 筛除心跳包
    x_need_cut = []
    for i in range(len(data_i)):
        if data_i[i] == data_q[i]:
            x_need_cut.append(i)
    for index in sorted(x_need_cut, reverse=True):
        del (data_i[index])
        del (data_q[index])
    return [data_i, data_q] if [data_i, data_q] else None


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


def f_readdata(load_path):
    # 以固定格式读数据文件
    data_list_i = []
    data_list_q = []
    v_freq = []
    pattern = r'-?\d+'
    with open(load_path, 'r') as file:
        for line in file:
            # 找频点
            num_freq = re.findall(r'find in (-?\d+)', line)
            if num_freq:
                v_freq.append(num_freq)
            num_line = re.findall(r'(-?\d+),(-?\d+)', line)
            # print(num_line)
            # 找数据
            if num_line:
                for match in num_line:
                    before_comma, after_comma = map(int, match)
                    data_list_i.append(before_comma)
                    data_list_q.append(after_comma)
    return [data_list_i, data_list_q, v_freq[0]] if [data_list_i, data_list_q, v_freq[0]] else None


def f_web_read(path):
    # 输入为fft和坐标临时文件所处的文件夹
    # 返回格式为[fft_abs, fft_axis]
    # path_write = 'C:\\Users\\%USERNAME%\\Desktop\\FWapp\\'
    file_write = 'FFT_' + 'result.txt'
    file_write2 = 'axis_' + 'result.txt'
    fft_abs = np.loadtxt(path + file_write)
    fft_axis = np.loadtxt(path + file_write2)
    return [fft_abs, fft_axis] if [fft_abs, fft_axis] else None


def f_data2fft_write(path_folder, path_write):
    file_lastest = f_find_latest_txt(path_folder)  # 自动找最新的文件
    # file_lastest = 'data722-1.txt'
    [data_i, data_q, freq_list] = f_readdata(path_folder + file_lastest)
    freq = (int(freq_list[0]))  # 读取到的中频
    bandwide = 40e6  # 固定设置的带宽
    [data_i, data_q] = f_de_tick(data_i, data_q)
    [data_i, data_q, time_stamp_idx1] = f_de_time_stamp(data_i, data_q)
    data = np.array(data_i) + 1j * np.array(data_q)
    data_fft = np.fft.fftshift(np.fft.fft(data))
    file_write = 'FFT_' + 'result.txt'
    file_write2 = 'axis_' + 'result.txt'
    data_fft_a = np.abs(data_fft)
    len_fft = len(data_fft_a)
    freq_axis = np.fft.fftshift(np.fft.fftfreq(len_fft, d=1 / bandwide)) + freq
    np.savetxt(path_write + file_write, data_fft_a, '%d')
    np.savetxt(path_write + file_write2, freq_axis, '%d')

def check_new(new_file):
    global last_file_name
    if new_file==last_file_name:
        return False
    else:
        last_file_name=new_file
        return True

if __name__ == '__main__':
    # load
    # 改成存储接收数据的文件夹
    path_folder = BaseConfig.DB_PATH + '/DATA/'
    # 改成FFT结果的临时存放文件夹
    path_write = BaseConfig.DB_PATH + '/'
    f_data2fft_write(path_folder, path_write)
    # 获取x和y轴
    [data_fft_a, freq_axis] = f_web_read(path_write)
    # 绘图
    plt.figure()
    plt.plot(freq_axis, data_fft_a)
    plt.show()
