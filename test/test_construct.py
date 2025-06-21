'''
@Project ：DroneContest 
@File    ：test_construct.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/21 9:51 
'''
from start import construct_baseconfig,load_config,scan_and_register

if __name__ == '__main__':
    load_config()
    scan_and_register()
    construct_baseconfig()