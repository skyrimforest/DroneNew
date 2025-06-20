# 调用此脚本以删除指定文件夹下以.grc结尾的文件
# 用于遍历
import os
# 获取项目路径
from geoDisturber.BaseConfig.base_config import BaseConfig
# 用于正则匹配
import re
def delete_grc(dir_name):
    grc_re=re.compile(r".*.grc$")
    abs_dir_name=BaseConfig.SCRIPTS_PATH+'/'+dir_name
    for root, dirs, files in os.walk(abs_dir_name):
        for file in files:
            if grc_re.match(file):
                abs_file_name=root+'/'+file
                os.remove(abs_file_name)

if __name__ == '__main__':
    # 递归移除FW_target的所有grc文件
    delete_grc("FW_target")


