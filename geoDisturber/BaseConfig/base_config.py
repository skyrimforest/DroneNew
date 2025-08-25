'''
@Project ：DroneContest 
@File    ：base_config.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/20 23:00 
'''
import os
import socket
from registry.registry import register_component


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


@register_component("geoDisturber.BaseConfig")
class BaseConfig:
    # 被动态设置的参数
    HOST_NAME = socket.gethostname()  # 自动从 socket.gethostname() 获取
    HOST_IP = get_host_ip()  # 自动从 get_host_ip() 获取，如需固定填入 "192.168.x.x"
    # HOST_IP = "192.168.1.200"
    # 自己的PROT
    HOST_PORT = 10002
    # 日志文件夹
    LOG_PATH = ROOT_DIR + '/loginfo'
    # 脚本文件夹
    SCRIPTS_PATH = ROOT_DIR + '/scripts'
    # 目标脚本文件夹
    # TARGET_SCRIPTS_PATH = 'FW_target'
    TARGET_SCRIPTS_PATH = 'My_test'
    # 目标脚本配置文件
    CONFIG_FILE = TARGET_SCRIPTS_PATH


if __name__ == '__main__':
    print(BaseConfig.HOST_NAME)
