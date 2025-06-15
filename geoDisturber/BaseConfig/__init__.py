import os
import socket

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


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


# 本机名称
HOST_NAME = socket.gethostname()
# 自己的IP
HOST_IP = get_host_ip()
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
