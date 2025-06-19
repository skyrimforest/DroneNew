'''
@Project ：DroneContest 
@File    ：decoder_util.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/19 19:49 
'''
from geoMaster.utils.decoder.src import droneid_receiver_offline
import argparse
import os
from datetime import datetime
import geoMaster.BaseConfig as BaseConfig

def decoder_offline(file_name):
    file_path=BaseConfig.DECODER_PATH+"/"+file_name
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gui', default=False, action="store_true", help="Show interactive")
    parser.add_argument('-i', '--input-file', default=file_path, help="Binary Sample Input")
    parser.add_argument('-s', '--sample-rate', default="50e6", type=float, help="Sample Rate")
    parser.add_argument('-l', '--legacy', default=False, action="store_true", help="Support of legacy drones (Mavic Pro, Mavic 2)")
    parser.add_argument('-d', '--debug', default=False, action="store_true", help="Enable debug output")
    parser.add_argument('-z', '--disable-zc-detection', default=True, action="store_false", help="Disable per-symbol ZC sequence detection (faster)")
    parser.add_argument('-f', '--skip-detection', default=False, action="store_true", help="Skip packet detection and enforce decoding of input file")
    args = parser.parse_args()

    return droneid_receiver_offline.dict_main(args)

def get_sample_file(directory):
    """扫描目录并获取文件信息"""
    if not os.path.exists(directory):
        print(f"错误: 目录 '{directory}' 不存在")
        return []

    file_info_list = []

    # 遍历目录中的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            try:
                # 获取文件的创建时间（时间戳）
                create_time = os.path.getctime(file_path)

                # 将时间戳转换为可读的日期时间格式
                create_datetime = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')

                # 收集文件信息
                file_info = {
                    'filename': filename,
                    'timestamp': create_datetime,
                }

                file_info_list.append(file_info)

            except Exception as e:
                print(f"无法获取文件 '{file_path}' 的信息: {e}")

    return file_info_list
