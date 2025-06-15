# 内存版本的tcp_client,与do_fft_memory配套

import socket
import time
import datetime
from SkyLogger import get_logger

from utils import do_fft_memory

logger = get_logger("tcp_client")


def get_client_socket():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_socket
    except:
        return None


# 和服务器连接
def connect_to_server(cli_socket, server_address):
    try:
        cli_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16 * 1024)
        cli_socket.connect(server_address)
        return {"success": True}
    except:
        return {"success": False}


def get_zed_info_from_tcp(cli_socket):
    command = cli_socket.recv(16)
    if command and command[0]:
        cmd_de = command.decode()
    else:
        return None
    if not (ord('A') <= ord(cmd_de[0]) <= ord('Z')):
        return None
    # logger.info(f"[test][get_zed_info_from_tcp]cmd:{cmd_de}")
    data_length = int(cmd_de.split()[1])
    # logger.info(f"[test][get_zed_info_from_tcp]length:{data_length}")
    recv_data = command + b"\n"
    for cnt in range(data_length):
        # time.sleep(0.1)
        data = cli_socket.recv(1*1024)
        recv_data = recv_data + data
    # logger.info(f"[test][get_zed_info_from_tcp]recv msg:{recv_data.rstrip()}")
    return recv_data.rstrip()


# 关闭
def close_socket(cli_socket):
    cli_socket.close()


if __name__ == '__main__':
    cli_socket = get_client_socket()
    connect_to_server(cli_socket, ('localhost', 8001))
    do_fft_memory.get_server_info_and_cut(cli_socket)
