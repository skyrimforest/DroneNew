import os
import re
from geoDisturber.BaseConfig.base_config import BaseConfig

import py_compile

def pyc_encode_scripts(dir_name):
    grc_re = re.compile(r".*.py$")
    abs_dir_name = BaseConfig.SCRIPTS_PATH + '/' + dir_name
    for root, dirs, files in os.walk(abs_dir_name):
        for file in files:
            if grc_re.match(file):
                abs_file_name = root + '/' + file
                target_dir = root
                res_file_name=target_dir + "/" + file + "c"
                py_compile.compile(abs_file_name, cfile=res_file_name)


def delete_all_pyfile(dir_name):
    # 在获取pyc文件后,递归删除所有的py文件
    grc_re = re.compile(r".*.py$")
    abs_dir_name = BaseConfig.SCRIPTS_PATH + '/' + dir_name
    for root, dirs, files in os.walk(abs_dir_name):
        for file in files:
            if grc_re.match(file):
                abs_file_name = root + '/' + file
                os.remove(abs_file_name)

def delete_all_grcfile(dir_name):
    grc_re=re.compile(r".*.grc$")
    abs_dir_name=BaseConfig.SCRIPTS_PATH+'/'+dir_name
    for root, dirs, files in os.walk(abs_dir_name):
        for file in files:
            if grc_re.match(file):
                abs_file_name=root+'/'+file
                os.remove(abs_file_name)

if __name__ == '__main__':
    dir_name=BaseConfig.SCRIPTS_PATH
    delete_all_grcfile(dir_name)
    pyc_encode_scripts(dir_name)
    delete_all_pyfile(dir_name)
