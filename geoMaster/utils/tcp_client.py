import socket
import os
import time
import datetime
from SkyLogger import get_logger

import BaseConfig

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


def do_data_save(recv_data, dataName=None):
    # 保证数据存储维持在10条
    # current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    current_time = dataName
    # 定义文件夹路径
    folder_path = os.path.join(BaseConfig.DB_PATH, 'DATA')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 定义文件名，使用时间作为文件名，并保存到data文件夹下
    file_name = os.path.join(folder_path, f"{current_time}.txt")
    # 将数据保存到 txt 文件
    with open(file_name, "wb") as file:
        file.write(recv_data)
    logger.info("data saved to {}".format(file_name))


def do_drone_data_save(recv_data, dataName=None):
    # 保证数据存储维持在10条
    # current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    current_time = dataName
    # 定义文件夹路径
    folder_path = os.path.join(BaseConfig.DB_PATH, 'DRONE_DATA')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 定义文件名，使用时间作为文件名，并保存到data文件夹下
    file_name = os.path.join(folder_path, f"{current_time}.txt")
    # 将数据保存到 txt 文件
    real_data_pre = recv_data.split()
    la_x = 39.912863418590014
    la_y = 116.39701366424
    real_data = f"{real_data_pre[0].decode()} {real_data_pre[-1].decode()} {la_x}_{la_y} {current_time}"
    with open(file_name, "wb") as file:
        file.write(real_data.encode())
    logger.info("data saved to {}".format(file_name))


def get_server_info_and_cut(cli_socket):
    while True:
        # 接收数据
        command = cli_socket.recv(16)
        print(command)
        data_length = int(command.decode().split()[1])
        cnt = 0
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        recv_data = b""
        if data_length > 0:
            while cnt < data_length:
                time.sleep(0.1)
                data = cli_socket.recv(1 * 1024)
                if cnt == 0:
                    info_list = data.split(b'\n')
                    do_drone_data_save(info_list[0], current_time)
                if cnt == data_length - 1:
                    data = data.rstrip()
                recv_data = recv_data + data
                cnt += 1
            do_data_save(recv_data, current_time)
        else:
            logger.info("data very small...")


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
        data = cli_socket.recv(1 * 1024)
        recv_data = recv_data + data
    # logger.info(f"[test][get_zed_info_from_tcp]recv msg:{recv_data.rstrip()}")
    return recv_data.rstrip()


# def get_server_info_and_cut(cli_socket):
#     while True:
#         # 接收数据
#         command = cli_socket.recv(16)
#         print(f"接收到指令:{command.decode()}")
#         data_length=int(command.decode().split()[1])
#         print(f"数据段长度:{data_length}")
#         current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
#         if data_length>0:
#             info = cli_socket.recv(1 * 1024)
#             info_list=info.split(b'\n')
#             do_drone_data_save(info_list[0], current_time)
#             data=cli_socket.recv((data_length-1) * 1024)
#             recv_data=info+data
#             do_data_save(recv_data, current_time)
#         else:
#             logger.info("data very small...")
#         time.sleep(1)


# 关闭
def close_socket(cli_socket):
    cli_socket.close()


if __name__ == '__main__':
    cli_socket = get_client_socket()
    connect_to_server(cli_socket, ('localhost', 8001))
    get_server_info_and_cut(cli_socket)
    # # 1 tcp_client_1
    # # AF_INET:IPV4, SOCK_STREAM:tcp, note:AF_INET6:IPV6
    #
    # tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    # # 2 Set Rcv Buff 1MB
    # tcp_client_1.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
    #
    # # 2 building link by connect
    # # argument:ip,port
    #
    # tcp_client_1.connect(('localhost', 8001))
    #
    # print("Now, Starting Recv Data From Serv:")
    # while True:
    #     # 4 recv bulk data
    #     recv_data = b""
    #     recv_count = 0
    #     while True:
    #         data = tcp_client_1.recv(1024 * 1024)
    #         # if not data:
    #         if data == 'hello':
    #             print("-------------------Finish----------------------------------")
    #             print("-data---:%s" % data)
    #             print("the process recv byte:%d, times:%d:" % (len(recv_data), recv_count))
    #             # print(recv_data)
    #             time.sleep(1)
    #             break
    #         recv_data += data
    #         recv_count += 1
    #         current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #         # 定义文件夹路径
    #         # folder_path = os.path.join(os.getcwd(), 'data')
    #         folder_path = os.path.join(BaseConfig.DB_PATH, 'data')
    #         if not os.path.exists(folder_path):
    #            os.makedirs(folder_path)
    #         # 定义文件名，使用时间作为文件名，并保存到data文件夹下
    #         file_name = os.path.join(folder_path, f"{current_time}.txt")
    #
    #         # 将数据保存到 txt 文件
    #         with open(file_name, "wb") as file:
    #             file.write(recv_data)
    #         print(recv_data)
    #         print("---------------------Recving------------------------------")
    #     print("waiting for next data from server:  ")
    #
    # # display recv_data by decode utf-8
    # print(recv_data.decode(encoding='utf-8'))
    #
    # # 5 cloase socker
    # tcp_client_1.close()

# 获取信息,使用了较为复杂的协议,不采用这版
# def get_server_info(cli_socket,info="start"):
#     try:
#         cli_socket.sendall(info.encode())
#
#         # 先接收4个字节长度(int型,代表消息长度)
#         len_bytes=cli_socket.recv(4)
#         info_len=int.from_bytes(len_bytes,byteorder='big')
#
#         # 再获取真的消息
#         data_bytes=cli_socket.recv(info_len)
#         real_data=data_bytes.decode()
#
#         print(real_data)
#         return {"success":True,
#                 "data":real_data}
#     except:
#         return {"success":False}
