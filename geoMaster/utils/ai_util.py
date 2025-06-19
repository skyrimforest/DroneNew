from geoMaster.utils.ASTGCN.test import main
import os
from datetime import datetime
import geoMaster.BaseConfig as BaseConfig

def ai_predict(file_name):
    file_path=BaseConfig.BIN_PATH+'/'+file_name
    return main(file_path)


def get_input_info(directory):
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

if __name__ == '__main__':
    # res=get_input_info(BaseConfig.BIN_PATH)
    # print(res)
    res=ai_predict(BaseConfig.BIN_PATH+'/UAV_5790_10')
    print(res)