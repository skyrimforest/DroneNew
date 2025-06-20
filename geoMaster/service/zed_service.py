# 负责与zed的通信等功能
import datetime
import re
# 用于同步机器时间
import subprocess
import threading
import time

import select

from geoMaster.BaseConfig.base_config import BaseConfig
from geoMaster.SkyLogger import get_logger
from geoMaster.schema.all_schema import CommGlobalPara
from geoMaster.utils import do_fft_memory, global_params, tdoa_tools_main, resolve_file, tcp_client_memory

# import child_service
# from child_service import get_x_y_from_child, get_drone_from_child

logger = get_logger("zed_service")


def get_marker_list():
    file_path = BaseConfig.DB_PATH + '/current_result.txt'
    return resolve_file.parse_json(file_path)


# 建立tcp连接 存储数据
def get_tcp_client_and_save_data():
    my_socket = tcp_client_memory.get_client_socket()
    while True:
        try:
            tcp_client_memory.connect_to_server(my_socket, (BaseConfig.ZED_IP, BaseConfig.ZED_PORT))
            do_fft_memory.get_server_info_and_cut(my_socket)
            logger.warning(f"Connection established, data trans start...")
        except Exception as e:
            logger.warning(f"{e} Now retrying...")
            time.sleep(BaseConfig.TCP_RETRY_TIME)


# 进行fft 获取xy
def do_fft_and_get_xy(sleep_time=BaseConfig.FFT_SLEEP_TIME):
    while True:
        try:
            time.sleep(sleep_time)
            file_latest = do_fft_memory.f_find_latest_txt()  # 自动找最新的文件
            if do_fft_memory.check_new(file_latest):
                do_fft_memory.f_data2fft_write()
                logger.info("fft done")
            else:
                logger.info("data not updated, no need to fft.")
        except Exception as e:
            logger.info(f"fft failed: {e}")


def run_fft():
    fft_thread = threading.Thread(target=do_fft_and_get_xy, )
    fft_thread.daemon = True
    fft_thread.start()
    logger.info("FFT Thread Started, do fft...")
    return fft_thread


def run_tcp_client_and_save_data():
    client_thread = threading.Thread(target=get_tcp_client_and_save_data, )
    client_thread.daemon = True
    client_thread.start()
    logger.info("TCP Client Started, waiting zed info to save...")
    return client_thread


# 获取FFT的结果数据
def get_frequency_data_master_memory():
    x = do_fft_memory.get_axis_result()
    y = do_fft_memory.get_fft_result()
    return x, y


'''
def get_frequency_data_child():
    # 从子节点获取x,y值
    # x_y_dicts = child_service.get_x_y_from_child()
    x_y_dicts = get_x_y_from_child()
    return x_y_dicts


def get_drone_data_child():
    # 从子节点获取新的无人机信息值
    # x_y_dicts,flag = child_service.get_drone_from_child()
    x_y_dicts, flag = get_drone_from_child()
    return x_y_dicts, flag
'''


# 直接获取zed线程全局变量名
def get_global_var_name_from_zed():
    child_name = "zed"
    child_ip = BaseConfig.ZED_IP
    child_port = BaseConfig.ZED_PORT
    child_global_var = child_name + '@' + child_ip + ':' + str(child_port)
    return child_global_var


# 设置本机时间
def set_current_time(date_stamp, time_stamp):
    # 形式为"YYYY-MM-DD"和"HH:MM:SS"
    ori_time = date_stamp + " " + time_stamp
    utc_time = datetime.datetime.strptime(ori_time, "%Y-%m-%d %H:%M:%S")
    utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
    local_time = utc_time.astimezone()
    target_stamp = local_time.strftime("%Y-%m-%d %H:%M:%S")

    # 使用 subprocess 调用 date 命令
    try:
        # 取消网络时间同步
        subprocess.run(["timedatectl", "set-ntp", "false"], check=True)
        # 设置当前系统时间
        subprocess.run(["timedatectl", "set-time", target_stamp], check=True)
        time.sleep(1)
        # print(f"系统时间已设置为: {target_stamp}")
    except subprocess.CalledProcessError as e:
        print(f"设置时间失败: {e}")


def zed_send_all(my_socket, data: str):
    total_sent = 0
    data = ''.join(data).encode('utf-8')
    while total_sent < len(data):
        sent = my_socket.send(data[total_sent:])
        if not sent:
            raise RuntimeError("socket broken")
        total_sent += sent


# 时间地理信息请求
def query_geo_from_zed(my_socket):
    logger.info('[t0219]p message has been sent')
    data = 'p               '
    try:
        # my_socket.sendall(''.join(data).encode('utf-8'))
        zed_send_all(my_socket, data)
    except Exception as e:
        logger.warning(f"{e} [test][comm_loop_zed:P:query]no connection")
        my_socket = tcp_client_memory.get_client_socket()
        tcp_result = tcp_client_memory.connect_to_server(my_socket, (BaseConfig.ZED_IP, BaseConfig.ZED_PORT))
        if not tcp_result["success"]:
            return None
    return my_socket


# zed通信线程
def communicate_loop_to_zed():
    global_params.set_str_data_to_global(get_global_var_name_from_zed(), CommGlobalPara())
    var_name = get_global_var_name_from_zed()
    my_socket = tcp_client_memory.get_client_socket()
    tcp_client_memory.connect_to_server(my_socket, (BaseConfig.ZED_IP, BaseConfig.ZED_PORT))
    # start_time = datetime.datetime.now()
    # my_socket = query_geo_from_zed(my_socket)
    while True:
        if my_socket:
            # 事先判断连接状态
            read_list, write_list, error_list = select.select([my_socket], [my_socket], [my_socket], 3)
        # 判断异常
        else:
            read_list = write_list = error_list = [my_socket]
        if (not my_socket) or my_socket in error_list:
            try:
                global_params.set_valid_from_global(var_name, False)
                my_socket = tcp_client_memory.get_client_socket()
                tcp_result = tcp_client_memory.connect_to_server(my_socket, (BaseConfig.ZED_IP, BaseConfig.ZED_PORT))
                if not tcp_result["success"]:
                    my_socket = None
                    logger.warning(f"[comm_loop_zed:error]Now retrying...")
                    continue
                else:
                    # my_socket = query_geo_from_zed(my_socket)
                    logger.info("[comm_loop_zed]reconnecting ...")
                    time.sleep(BaseConfig.TCP_RETRY_TIME)
            except Exception as e:
                logger.warning(f"{e} [comm_loop_zed:error]Now retrying...")
                # time.sleep(BaseConfig.TCP_RETRY_TIME)
            continue
        # 读zed
        if my_socket in read_list:
            try:
                data = tcp_client_memory.get_zed_info_from_tcp(my_socket)
                # start_time = datetime.datetime.now()
                recv_process(var_name, data)
            except Exception as e:
                # logger.warning(f"{temp_data[0:min(len(temp_data),3)]}")  # 测试用
                logger.warning(f"{e} [comm_loop_zed:read]Now retrying...")
                global_params.set_valid_from_global(var_name, False)
                # my_socket = tcp_client_memory.get_client_socket()
                # tcp_client_memory.connect_to_server(my_socket, (BaseConfig.ZED_IP, BaseConfig.ZED_PORT))
                my_socket = None
        # else:
        #     end_time = datetime.datetime.now()
        #     if (end_time - start_time).seconds > BaseConfig.ZED_OVER_TIME:
        #         start_time = datetime.datetime.now()
        #         my_socket = query_geo_from_zed(my_socket)
        # 发指令
        if my_socket in write_list:
            [_, flag_send] = global_params.query_queue_data_exist(var_name)
            if flag_send:
                if data := global_params.get_queue_tosend_data_from_global(var_name):
                    try:
                        logger.info(f"[comm_loop_zed:send]Connection established, data trans start...")
                        my_socket.sendall(''.join(data).encode('utf-8'))
                        # zed_send_all(my_socket, data)
                        # start_time = datetime.datetime.now()
                    except Exception as e:
                        logger.warning(f"{e} [comm_loop_zed:send]Now retrying...")
                        # global_params.set_queue_tosend_data_to_global(var_name, data)  # 没发送成功就放回去
                        global_params.set_valid_from_global(var_name, False)
                        # my_socket = tcp_client_memory.get_client_socket()
                        # tcp_client_memory.connect_to_server(my_socket, (BaseConfig.ZED_IP, BaseConfig.ZED_PORT))
                        my_socket = None
        # end_time = datetime.datetime.now()
        # if my_socket:
        #     if (end_time - start_time).seconds > BaseConfig.ZED_OVER_TIME:
        #         start_time = datetime.datetime.now()
        #         my_socket = query_geo_from_zed(my_socket)


# 接收信息处理
def recv_process(var_name: str, data: bytes):
    if data:
        data: str = data.decode()
        # D message
        if data.startswith('D:'):
            recv_process_d(var_name, data)
        # I message
        elif data.startswith('I:'):
            recv_process_i(var_name, data)
        # E message
        elif data.startswith('E:'):
            recv_process_e(var_name, data)
        # P message
        elif data.startswith('P:'):
            recv_process_p(var_name, data)
        # others
        else:
            pass


# D消息处理
def recv_process_d(var_name: str, data: str):
    logger.info(f"[comm_loop_zed:read]msg mode:D")
    temp_data = data.split('\n')
    logger.info(f"{temp_data[0]}")
    # 存入形式：f"D XX\nI:for toa\n12,63\n0,20241\n300,0\n-52,3\n-20,-301"
    # 存入形式：f"D XX\nfor zc\n1\n10000\n50000\n200000\n1000000"
    global_params.set_queue_gotten_data_to_global(var_name, '\n'.join(temp_data[1:]))


# I消息处理
def recv_process_i(var_name: str, data: str):
    logger.info(f"[comm_loop_zed:read]msg mode:I")
    temp_data = data.split('\n')
    # 存入形式：f"5800000000\n536"
    data = ['findmsg', 0, 0]
    for content in temp_data[1:]:
        match_freq = re.search(r'findin\s*(\d+)', content)
        match_D = re.search(r'findin\sd\s*(\d+)', content)
        if match_freq:
            data[1] = match_freq.group(1)
        elif match_D:
            data[2] = match_D.group(1)
    global_params.set_queue_gotten_data_to_global(var_name, '\n'.join(data))


# E消息处理
def recv_process_e(var_name: str, data: str):
    if "no_pps" not in data:
        logger.info(f"[comm_loop_zed:read]msg mode:E:{data}")
        # [t0217]取消zed错误端口
        # global_params.set_valid_from_global(var_name, False)
    else:
        logger.info(f"[comm_loop_zed:read]msg mode:E:{data}")


# P消息处理
def recv_process_p(var_name: str, data: str):
    logger.info(f"[comm_loop_zed:read]msg mode:P")
    temp_data = data.split('\n')
    try:
        content = temp_data[2]
        data_match = re.search(r'(\d{1,3}).(\d{1,2}\.\d+)\'\s*([A-Za-z])', content)
        if data_match:
            if data_match.group(3) == 'N':
                deg = 1
            elif data_match.group(3) == 'S':
                deg = -1
            else:
                raise ValueError("纬度信息为空")
            deg *= int(data_match.group(1))
            temp_minute = float(data_match.group(2))
            minute = int(temp_minute // 1)
            second = round((temp_minute - minute) * 60, 5)
            B_list = [deg, minute, second]
        else:
            raise ValueError("纬度信息为空")
        # 经度信息
        content = temp_data[3]
        data_match = re.search(r'(\d{1,3}).(\d{1,2}\.\d+)\'\s*([A-Za-z])', content)
        if data_match:
            if data_match.group(3) == 'E':
                deg = 1
            elif data_match.group(3) == 'W':
                deg = -1
            else:
                raise ValueError("经度信息为空")
            deg *= int(data_match.group(1))
            temp_minute = float(data_match.group(2))
            minute = int(temp_minute // 1)
            second = round((temp_minute - minute) * 60, 5)
            L_list = [deg, minute, second]
        else:
            raise ValueError("经度信息为空")
        # 高度信息
        content = temp_data[4]
        data_match = re.search(r'([-+]?\d+\.\d+)', content)
        if data_match:
            H_list = float(data_match.group())
        else:
            raise ValueError("高度信息为空")
        # 同步本地信息
        res_geo = tdoa_tools_main.po2str(H_list, B_list, L_list)  # 获取的授时位置
        BaseConfig.host_address = res_geo
        BaseConfig.FLAG_LOCAL_ADDRESS = True
        logger.info(f"geo:{res_geo}")

    except ValueError as e:
        logger.warning(f"[comm_loop_zed:read]msg mode:P address,error:{e}")
        if not BaseConfig.FLAG_LOCAL_ADDRESS:
            global_params.set_valid_from_global(var_name, False)
    try:
        # 日期、时间信息
        content = temp_data[5]
        data_match_t = re.search(r'[0-2]?[0-9]:[0-5][0-9]:[0-5][0-9]', content)
        data_match_d = re.search(r'\d{4}-\d{2}-\d{2}', content)
        if data_match_d and data_match_t:
            # 形式为"YYYY-MM-DD"和"HH:MM:SS"
            res_date: str = data_match_d.group()
            res_time: str = data_match_t.group()
            set_current_time(res_date, res_time)
            BaseConfig.FLAG_LOCAL_TIME = True
            logger.info(f"date:{res_date},{res_time}")
        else:
            raise ValueError("时间信息为空")
    except ValueError as e:
        logger.warning(f"[comm_loop_zed:read]msg mode:P time,error:{e}")
        if not BaseConfig.FLAG_LOCAL_TIME:
            global_params.set_valid_from_global(var_name, False)


if __name__ == '__main__':
    # get_drone_data()
    pass
