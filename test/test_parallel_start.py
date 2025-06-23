'''
@Project ：DroneContest 
@File    ：test_parallel_start.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/23 22:51 
'''

from start_parallel import construct_baseconfig,load_config,scan_and_register,start_front

if __name__ == '__main__':
    load_config()
    scan_and_register()
    construct_baseconfig()
    start_front()

