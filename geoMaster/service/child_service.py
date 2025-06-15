# 负责与child板卡通信等功能,系统共有三个子板卡,后续还可能继续扩展

import json
# 引入http
import requests
# 引入日期
import datetime
# 引入基本配置
import geoMaster.BaseConfig as BaseConfig
# 引入子节点信息类型
from geoMaster.schema.all_schema import ChildInfo, PureInfo, CommGlobalPara
# 引入child数据库操作
from geoMaster.mapper import child_mapper
# 引入日志
from geoMaster.SkyLogger import get_logger
# 引入后台任务
from fastapi import BackgroundTasks
from geoMaster.API import child_api
from geoMaster.utils import global_params

logger = get_logger("child_service")
test_ci = ChildInfo(
    child_name="skyrim-child01",
    child_ip="localhost",
    child_port="10001",
    child_geo="233_344_233_344_233_344_0")

# 这里维护的是动态注册的所有节点
child_dict = {}


# 上次更新在3分钟之内 则节点在线
def check_child_online(ci):
    curr_time = datetime.datetime.now()
    time_before = ci["start_time"]
    delta = curr_time - time_before
    if delta.total_seconds() < BaseConfig.REGISTER_CHECK_TIME:
  # 缩减边界时间至2次注册，便于同步
        return True
    else:
        return False


# 本函数用于在所有节点操作之前进行判断,
# 需要对节点进行过期判断,180s没有更新就判断为过期
# 返回存活的child_list
def check_child_info():
    global child_dict
    new_child_list = []
    for _, child in list(child_dict.items()):
        if check_child_online(child):
            new_child_list.append(child)
    return new_child_list


# 返回当前在线的节点列表 适应前端做了适配
def get_connected_child_info():
    global child_dict
    new_child_list = []
    for _, child in list(child_dict.items()):
        child_data = {}
        child_data["name"] = child["uuid"]
        child_data["lastupdate"] = child["start_time"].strftime("%m-%d %H:%M:%S")
        new_child_list.append(child_data)
    # print(new_child_list)
    return new_child_list


# 返回当前所有在线的节点列表 适应前端做了适配
def get_node_info():
    res_list = []
    master_data = {
        "node_name": BaseConfig.HOST_NAME,
        "node_ip": BaseConfig.HOST_IP,
        "node_port": BaseConfig.HOST_PORT,
        "last_updated": datetime.datetime.now().strftime("%m-%d %H:%M"),
        "geo_place": BaseConfig.host_address
    }
    res_list.append(master_data)
    # todo 处理一下子节点相关
    return res_list


# 子板卡向父节点注册自己,以便发送信息 使用uuid进行唯一辨识
def child_register(ci: ChildInfo):
    global child_dict
    child_name = ci.child_name
    child_ip = ci.child_ip
    child_port = ci.child_port

    uuid = child_name + "@" + child_ip + ":" + child_port
    child_data = {
        "uuid": uuid,
        "child_name": child_name,
        "child_ip": child_ip,
        "child_port": child_port,
        "start_time": datetime.datetime.now(),
        "child_geo": get_geo_location(ci)
    }
    if uuid not in child_dict:
        child_dict[uuid] = child_data
        logger.info(f"{uuid} registered")
        global_params.set_str_data_to_global(get_var_name(uuid), CommGlobalPara(valid=False))
        logger.info(f"{uuid} create its global_para:{get_var_name(uuid)}")
    elif child_dict[uuid] not in check_child_info():
        child_dict[uuid]["child_geo"] = child_data["child_geo"]
        child_dict[uuid]["start_time"] = child_data["start_time"]
        logger.info(f"{uuid} reregistered")
        global_params.set_str_data_to_global(get_var_name(uuid), CommGlobalPara(valid=False))
        logger.info(f"{uuid} recreate its global_para:{get_var_name(uuid)}")
    else:
        time_before = child_dict[uuid]["start_time"]
        time_after = datetime.datetime.now()
        delta = time_after - time_before
        child_dict[uuid]["start_time"] = time_after
        logger.info(f"{uuid} last update {delta} ago, now it's re-updated.")
        # logger.info(f"[test]child online:{check_child_info()}")
        child_dict[uuid]["child_geo"] = child_data["child_geo"]


# 从ci中获取url
def get_url_from_ci(ci: dict):
    child_ip = ci["child_ip"]
    child_port = ci["child_port"]
    child_url = "http://" + child_ip + ":" + child_port
    return child_url


# 父板卡向单个子板卡发送信息
def send_info_single(ci, data: dict):
    # 调用recv这个API进行发送
    child_url = get_url_from_ci(ci) + child_api.API['recv']
    data_packet = {
        "info": data
    }
    # try:
    res = requests.post(child_url, json=data_packet)
    # logger.info(f"sent done {res.text} and content:{data}")
    # except Exception as e:
    #     logger.info(f"{e} sent failed ")


# 父板卡向全部子板卡发送信息 可以用后续的do_ope函数实现
def send_info_child(data: dict, bt: BackgroundTasks):
    global child_dict
    for _, child in child_dict.items():
        bt.add_task(send_info_single, child, data)
    logger.info(f"info sent to all {len(child_dict)} child")


# 父板卡向单个子板卡询问频率信息
def get_x_y_from_child_single(ci):
    child_url = get_url_from_ci(ci) + child_api.API['frequency']
    res = requests.post(child_url)
    child_item = {
        "name": ci['uuid'],
        "data": json.loads(res.text)
    }
    logger.info(f"frequency got from {ci['uuid']}")
    return child_item


# 从所有子节点获取x,y值
# 返回值为字典类型的数组,记录每个子节点的信息
def get_x_y_from_child():
    global child_dict
    res_dicts = []
    for _, child in child_dict.items():
        res_dicts.append(get_x_y_from_child_single(child))
    logger.info(f"frequency got from all {len(child_dict)} child")
    return res_dicts


# 通过child_geo字段返回x,y坐标
def get_geo_location(ci):
    child_geo = ci.child_geo.split("_")
    child_H = float(child_geo[0])
    child_B = [float(child_geo[1]), float(child_geo[2]), float(child_geo[3])]
    child_L = [float(child_geo[4]), float(child_geo[5]), float(child_geo[6])]
    # child_y = child_geo[1]
    return [child_H, child_B, child_L]


# 返回主站已记录的子站信息
def get_child_info():
    global child_dict
    return child_dict


# 获取私有变量名
def get_var_name(uuid, var_name=global_params.BUFFERS):
    # 获取前缀
    prefix = uuid
    # 拼接产生子站私有的变量名称
    child_var_name = prefix + var_name
    return child_var_name


# 主节点设置要发送的数据
def master_set_data2send(uuid, data):
    queue2send = get_var_name(uuid, global_params.BUFFERS)
    global_params.set_queue_tosend_data_to_global(queue2send, data)


# 主节点获得要发送的数据
def master_get_data2send(uuid, mark: bool = True):
    queue2send = get_var_name(uuid, global_params.BUFFERS)
    data2send = global_params.get_queue_tosend_data_from_global(queue2send, mark)
    return data2send


# 主节点设置要接收的数据
def master_set_data2recv(uuid, data):
    queue2recv = get_var_name(uuid, global_params.BUFFERS)
    global_params.set_queue_gotten_data_to_global(queue2recv, data)


# 主节点获得要接收的数据
def master_get_data2recv(uuid, mark: bool = True):
    queue2recv = get_var_name(uuid, global_params.BUFFERS)
    data2recv = global_params.get_queue_gotten_data_from_global(queue2recv, mark)
    return data2recv


# 查询单个子站是否有到达的信息 ci为单个节点的消息
def query_child_single(ci):
    uuid = ci['uuid']
    queue2recv = get_var_name(uuid, global_params.BUFFERS)
    return global_params.query_queue_data_exist(queue2recv)[0]  # 只检查到达


# 接收单个子站信息
def fetch_child_single(ci, cmd: bool = True):
    uuid = ci['uuid']
    queue2recv = get_var_name(uuid, global_params.BUFFERS)
    return global_params.get_queue_gotten_data_from_global(queue2recv, cmd)


# 向单个子节点对应的发送缓冲区中添加数据
def add_info_to_queue_single(ci, data):
    # 获取前缀
    prefix = ci['uuid']
    # 拼接产生子站私有的变量名称
    queue_to_sent = prefix + global_params.BUFFERS
    global_params.set_queue_tosend_data_to_global(queue_to_sent, data)


# 获取单个子站缓冲区的有效性（是否有高优先度标识
def fetch_valid_single(ci):
    prefix = ci['uuid']
    queue_to_sent = prefix + global_params.BUFFERS
    return global_params.get_valid_from_global(queue_to_sent)


# 重启状态中的初始化
def invalid_mode_init_single(ci):
    prefix = ci['uuid']
    queue_to_sent = prefix + global_params.BUFFERS
    global_params.get_queue_tosend_data_from_global(queue_to_sent, False)
    global_params.set_valid_from_global(queue_to_sent, True)


# 获取发送缓冲区中的数据并真正发送出去
def buffer_data_send_single(ci):
    uuid = ci['uuid']
    data2send: PureInfo = master_get_data2send(uuid)
    # 没有数据就直接返回
    if data2send is None:
        logger.info("send buffer is void...")
        return
    # 有数据就发送
    data = {
        "uuid": uuid,  # 节点标识
        "data": data2send.info
    }
    send_info_single(ci, data)
    logger.info("one info sent...")


# 在子节点上做操作,传入一类函数ope_func作为回调,
# ope_func类函数均需要接受ci作为参数,编码格式上均应以single结尾
# 可能需要传输数据,按顺序或var=value格式传都可
def do_ope_on_child(ope_func, *args, **kwargs):
    # global child_dict
    child_list = check_child_info()
    res = []
    for child in child_list:
        res.append(ope_func(child, *args, **kwargs))
    # logger.info(f"{ope_func.__name__} did for all {len(child_dict)} child")
    return res


if __name__ == '__main__':
    # get_x_y_from_child()
    # data2wrap = {
    #     "uuid": 233,  # 节点标识
    #     "data": 233
    # }
    # data_packet = PureInfo(info=data2wrap)
    # print(data_packet)
    test_ci = ChildInfo(
        child_name="fallen-child01",
        child_ip="localhost",
        child_port="10001",
        child_geo="6907.435_25_41_10.6773_123_22_17.0189")
    child_register(test_ci)
    ci_list = get_child_info()
    for ci in ci_list.values():
        a = ci["child_geo"]
        print(ci["child_geo"])
