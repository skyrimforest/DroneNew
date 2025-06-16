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


# 日志文件夹
LOG_PATH = ROOT_DIR + '/loginfo'
DB_PATH = ROOT_DIR + '/db'
BIN_PATH=ROOT_DIR + '/utils/ASTGCN/dataset'
AI_PIC_PATH = ROOT_DIR + '/utils/ASTGCN/test_images'


# 启动参数
ARGS = None
# 本机名称
HOST_NAME = socket.gethostname()
# 自己的IP
HOST_IP = get_host_ip()
# HOST_IP = "192.168.1.30"
# 自己的PROT
HOST_PORT = 10000
# 自己的地址
host_address = '0_0_0_0_0_0_0'
# 时区补正（基于UTC）
TIME_ZONE = 8
# zed板卡的IP
# ZED_IP = "127.0.0.1"
ZED_IP = "192.168.1.10"
# zed板卡的PORT
ZED_PORT = 7
# OS root password
ROOT_PASSWORD = '111111'

# 时间参数
# 前端推送时间
WEBSOCKET_TIME = 5
# 波形频率更新时间
FREQUENCY_UPDATE_TIME = 3
# 子站检测时间间隔
REGISTER_CHECK_TIME = 15
# TCP连接重试时间
TCP_RETRY_TIME = 3
# 多长时间做一次FFT
FFT_SLEEP_TIME = 3.5
# 最多保留多少个原始数据文件
RESERVED_FILE_NUMBER = 10
# 最少需要启动的子站数
MIN_STATION_NUM = 1
# 线程循环默认等待时间
LOOP_WAIT_TIME = 0.5
# SET指令的默认滞后时间（s）
SET_DELAY_TIME = 10
# 循环超时时间
WAIT_OVER_TIME = 15
# 通信超时时间
ZED_OVER_TIME =20

# 处理中参数
# 索引提前
INDEX_MOVE = 5120
# 本站地址标志位
FLAG_LOCAL_ADDRESS = False
# 本站时间标志位
FLAG_LOCAL_TIME = False

# 缓冲区标准指令集
# 主对子
INS_RESTART = "CMD:0:RESTART"  # 全站重启
INS_START = "CMD:1:START"  # 状态0启动
# 子对主
INS_ERROR = "CASE:0:ERROR"  # 错误上报
INS_WAIT = "CASE:1:WAITING"  # 等待响应
