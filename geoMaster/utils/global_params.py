'''
@Project ：pyfw01
@File    ：global_params.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/11/6 21:23 
'''

import threading
import queue
from geoMaster.schema import all_schema

# 为了与http服务建立联系,需要在此设置全局变量

# 采用的全局变量表,注意及时更新
NEW_DATA_QUEUE = "NEW_DATA_QUEUE"  # 接收缓冲区队列
CHILD_DICT = "CHILD_DICT"  # 已注册且未过期的子节点

# 对于下列变量来说,其为每个子节点私有,从全局区获取时 uuid+变量名 即可
BUFFERS = "BUFFERS"  # 发送缓冲区+接收缓冲区

lock = threading.Lock()


# 查询全局通信变量是否存在，并返回其当前状态：[接收位，发送位]是否有信息滞留
# 命名为queue_name 虽然不止有queue 但逻辑上只有一个queue受到影响
def query_queue_data_exist(queue_name):
    exist = [False, False]
    with lock:
        cur_CommPara = globals().get(queue_name, None)  # 自带的全局字典
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):  # 顺便验证类型
        with cur_CommPara.lock:  # 读取到后就转用变量内的锁，降低全局字典占用时间
            if not cur_CommPara.msg_gotten.empty():
                exist[0] = True
            if not cur_CommPara.msg_tosend.empty():
                exist[1] = True
    return exist


# 从接收缓冲区获取data,模式False时清空
def get_queue_gotten_data_from_global(queue_name, mode: bool = True):
    with lock:
        cur_CommPara = globals().get(queue_name, None)
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):
        with cur_CommPara.lock:
            if mode:
                try:
                    data = cur_CommPara.msg_gotten.get(block=False)  # 没有时不等待
                except queue.Empty:
                    data = None
                return data
            else:
                while not cur_CommPara.msg_tosend.empty():
                    cur_CommPara.msg_tosend.get()
    return None


# 从发送缓冲区获取data,模式False时清空
def get_queue_tosend_data_from_global(queue_name, mode: bool = True):
    with lock:
        cur_CommPara = globals().get(queue_name, None)
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):
        with cur_CommPara.lock:
            if mode:
                try:
                    data = cur_CommPara.msg_tosend.get(block=False)  # 没有时不等待
                except queue.Empty:
                    data = None
                return data
            else:
                while not cur_CommPara.msg_tosend.empty():
                    cur_CommPara.msg_tosend.get()
    return None


# 从缓冲区获取标识位
def get_valid_from_global(queue_name):
    data = False
    with lock:
        cur_CommPara = globals().get(queue_name, None)
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):
        with cur_CommPara.lock:
            data = cur_CommPara.valid
    return data


# 向接收缓冲区填入data
def set_queue_gotten_data_to_global(queue_name, data):
    with lock:
        cur_CommPara = globals().get(queue_name, None)
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):
        with cur_CommPara.lock:
            if data:  # 防止空指令
                cur_CommPara.msg_gotten.put(data)


# 向发送缓冲区填入data
def set_queue_tosend_data_to_global(queue_name, data):
    with lock:
        cur_CommPara = globals().get(queue_name, None)
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):
        with cur_CommPara.lock:
            if data:
                cur_CommPara.msg_tosend.put(data)
    else:
        print('cant find para')


# 向缓冲区标识位写入
def set_valid_from_global(queue_name, mark: bool):
    with lock:
        cur_CommPara = globals().get(queue_name, None)
    if cur_CommPara and isinstance(cur_CommPara, all_schema.CommGlobalPara):
        with cur_CommPara.lock:
            cur_CommPara.valid = mark


# 查询某个变量是否存在,存在返回true，否则返回false
# 变量可能存在(true),可能不存在(false),可能存在但已经被消耗就置为None(false)
# 更一般的查询变量是否存在（有CommGlobalPara类之后就可能用不上了）
def query_str_data_exist(data_name):
    with lock:
        cur_CommPara = globals().get(data_name, None)
    return True if cur_CommPara else False


# 传入字符串,返回相应的变量
# 避免线程问题需要加锁
# 查询，返回变量本身
def get_str_data_from_global(data_name):
    with lock:
        cur_CommPara = globals().get(data_name, None)
    return cur_CommPara


# 设定对应的变量
# 避免线程问题需要加锁
# 初始化对应变量（重复则替换）
def set_str_data_to_global(data_name, data):
    with lock:
        globals()[data_name] = data


if __name__ == '__main__':
    data = "set d        536set d        536set d        536set d        536"
    data2 = "find xxx in 5800000000"
    test_cgp = all_schema.CommGlobalPara()
    thread = threading.Thread(target=set_str_data_to_global, args=("test01", test_cgp))
    thread.start()
    print((query_queue_data_exist('test01')))
    thread = threading.Thread(target=set_queue_tosend_data_to_global, args=("test01", data))
    thread.start()
    thread = threading.Thread(target=set_queue_gotten_data_to_global, args=("test01", data2))
    thread.start()
    print((query_queue_data_exist('test01')))
    [b1, b2] = (query_queue_data_exist('test01'))
    if b1:
        data3 = get_queue_gotten_data_from_global('test01')
        print(data3)
    print((query_queue_data_exist('test01')))
    a = ["test01"]
    thread = threading.Thread(target=get_queue_gotten_data_from_global, args=a)
    thread.start()
    thread = threading.Thread(target=get_queue_tosend_data_from_global, args=a)
    thread.start()
    print((query_queue_data_exist('test01')))
    thread.join()
