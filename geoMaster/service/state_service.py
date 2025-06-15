import datetime
import time
from typing import Optional

import geoMaster.BaseConfig as BaseConfig
from geoMaster.schema.all_schema import ZedOrderSET, ZedOrderNED, Task, PureInfo
from geoMaster.service import zed_service, child_service
from geoMaster.utils import tdoa_tools_main as local_service, global_params, do_fft_memory
from geoMaster.SkyLogger import get_logger

logger = get_logger("state_service")
comm_thread_name_zed: str = zed_service.get_global_var_name_from_zed()
global_mark_error: int = 0
freq_send: int = 0


# 状态间变量


def control_loop():
    counter: Task = Task(loop_max_num=4)
    while True:
        while counter.get_state() == 0:
            counter = state_0_main(counter)
        while counter.get_state() == 1:
            counter = state_1_main(counter)
        while counter.get_state() == 2:
            counter = state_2_main(counter)
        while counter.get_state() == 3:
            counter = state_3_main(counter)
        while not counter.valid_check():
            counter = state_e_main(counter)
            # # 异常状态处理


def state_0_main(counter: Task) -> Task:
    # 启动状态
    # 检查站数，等待到齐
    if len(child_service.check_child_info()) >= BaseConfig.MIN_STATION_NUM:
        all_flag: Optional[list[bool]] = child_service.do_ope_on_child(child_service.fetch_valid_single)
        if all_flag and not all(all_flag):
            counter.set_state(-1)
            return counter
        # 向所有子站发启动信息
        # 清空子站到达消息
        child_service.do_ope_on_child(child_service.fetch_child_single, False)
        # 广播 S0
        try:
            send_to_all(BaseConfig.INS_START)  # 广播消息
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
            counter.mark["son"]: bool = True
        except Exception as e:
            logger.warning("some sons are not right")
            counter.set_state(-1)
            return counter
    # zed异常处理
    if not global_params.get_valid_from_global(queue_name=comm_thread_name_zed):
        logger.warning("status of zed is not right")
        counter.set_state(-1)
        return counter
    # 子站异常处理
    all_flag: Optional[list[bool]] = child_service.do_ope_on_child(child_service.fetch_valid_single)
    if all_flag and not all(all_flag):
        logger.warning("status of sons is not right")
        counter.set_state(-1)
        return counter
    # 重启操作执行完，下一状态
    if counter.mark["son"]:
        if counter.valid_check():
            # 清空接收队列
            global_params.get_queue_gotten_data_from_global(queue_name=comm_thread_name_zed, mode=False)
            logger.info("mode changed into 1")
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
            counter.next_state()  # 切换状态
    return counter


def state_1_main(counter: Task) -> Task:
    # 状态1数据位置安排：
    # 1号槽：zed报文
    # 2号槽：子站报文
    # 3号槽：指令
    global freq_send
    # [未收到子站信息][未收到zed信息]等待接收zed发现目标信息
    if not counter.get_cnt_1() and not counter.get_cnt_2():
        if global_params.query_queue_data_exist(queue_name=comm_thread_name_zed)[0]:  # zed到达消息
            data: str = global_params.get_queue_gotten_data_from_global(queue_name=comm_thread_name_zed)
            if data.startswith("findmsg"):  # 检验格式
                data: list[str] = data.split('\n')
                counter.set_content_1(cnt=data[1:])  # 更新counter内容
                data: list[int] = [int(k) for k in data[1:]]
                # DONE:[未收到子站信息][收到zed信息]生成SET指令，线程信息同步
                temp_CMD = state1_data_to_cmd_set(data=data)  # DONE:信息转指令
                if not counter.get_cnt_3():
                    freq_send = data[0]
                    counter.set_content_3(cnt=temp_CMD)  # 指令存到3号槽
                if not temp_CMD:
                    counter.new_cnt1()
    # [未收到zed信息][未收到子站信息]等待接受子站的发现目标信息
    if not counter.get_cnt_1() and not counter.get_cnt_2():
        for cii in child_service.check_child_info():
            if child_service.query_child_single(cii) and not counter.get_cnt_1() and not counter.get_cnt_2():
                data: dict = child_service.fetch_child_single(cii)
                counter.set_content_2(cnt=data.get("info", None) if data else None)
        if counter.get_cnt_2():
            data: str = counter.get_content_2()
            if data.startswith("findmsg"):  # 检验格式
                data: list[str] = data.split('\n')
                data: list[int] = [int(k) for k in data[1:]]
                temp_CMD: Optional[str] = state1_data_to_cmd_set(data)
                if not counter.get_cnt_3():
                    freq_send = data[0]
                    counter.set_content_3(temp_CMD)  # 指令存到3号槽
                if not temp_CMD:
                    counter.new_cnt2()
            else:
                counter.new_cnt2()
    # [已有指令]向子站发送SET指令
    if counter.get_cnt_3():
        try:
            send_to_all(counter.get_content_3())  # 广播消息
        except Exception as e:
            logger.warning(f"[s1]{e}:send to sons failed")
            counter.set_state(-1)
            return counter
        counter.mark["son"]: bool = True

    # [已有指令]向zed发送指令
    if counter.get_cnt_3():
        logger.info(f"[test]send to zed:{counter.get_content_3()}")
        global_params.set_queue_tosend_data_to_global(
            queue_name=comm_thread_name_zed, data=counter.get_content_3()
        )
        counter.mark["zed"]: bool = True
    # 异常处理
    if not valid_detect():
        counter.set_state(-1)
        return counter
    # [发送指令结束]切换到下一状态
    if counter.mark["zed"] and counter.mark["son"]:
        if counter.valid_check():
            logger.info("mode changed into 2")
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
            counter.next_state()  # 切换状态
    return counter


def state_2_main(counter: Task) -> Task:
    # 状态2数据位置安排：
    # 1号槽：zed索引组/zed索引
    # 2号槽：子站索引组列表
    # 3号槽：子站目标索引列表
    # [未收到zed信息]等待接收zed的索引信息
    global global_mark_error
    if not counter.get_cnt_1():
        start_time = datetime.datetime.now()
        while True:
            if global_params.query_queue_data_exist(queue_name=comm_thread_name_zed)[0]:  # zed到达消息
                data: str = global_params.get_queue_gotten_data_from_global(comm_thread_name_zed)
                if data.startswith("D_time_upload"):
                    data: list[str] = data.split('\n')  # 转换为数组
                    data: list[str] = data[1:]
                    counter.set_content_1(cnt=data)
                    break
            end_time = datetime.datetime.now()
            delta_time: datetime.timedelta = end_time - start_time
            # 超时case
            if delta_time.seconds > BaseConfig.WAIT_OVER_TIME:  # 2*BaseConfig.SET_DELAY_TIME:
                counter.set_state(-1)
                logger.warning('[error][s2]state over time')
                return counter  # 异常跳出
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
            # 异常出口，超时报错跳出
    # [收到子站信息]接收子站索引组（记录顺序）
    if not counter.get_cnt_2():
        start_time: datetime = datetime.datetime.now()
        data: list = []
        while not child_service.check_child_info():
            end_time: datetime = datetime.datetime.now()
            delta_time: datetime.timedelta = end_time - start_time
            # 超时case
            if delta_time.seconds > BaseConfig.WAIT_OVER_TIME:  # 2*BaseConfig.SET_DELAY_TIME:
                logger.warning("[s2]wait son num over time")
                counter.set_state(-1)
                return counter
        for ci in child_service.check_child_info():
            temp: None = None
            if child_service.query_child_single(ci):
                temp: dict = child_service.fetch_child_single(ci)
                logger.info(temp) # t0217
                temp: Optional[str] = temp.get("info", None)
            while (not temp) or not temp.startswith("D_time_upload"):
                time.sleep(BaseConfig.LOOP_WAIT_TIME)
                # flag: bool = child_service.query_child_single(ci)
                if child_service.query_child_single(ci):
                    temp: dict = child_service.fetch_child_single(ci)
                    temp: Optional[str] = temp.get("info", None) if temp else None
                
                end_time: datetime = datetime.datetime.now()
                delta_time: datetime.timedelta = end_time - start_time
                # 超时case
                if delta_time.seconds > BaseConfig.WAIT_OVER_TIME:  # 2*BaseConfig.SET_DELAY_TIME:
                    logger.warning("[s2]son loop over time")
                    counter.set_state(-1)
                    return counter  # 异常跳出
            temp: Optional[list[str]] = temp.split('\n') if temp else None
            data.append(temp[1:])
        if data and counter.valid_check():
            counter.set_content_2(data)  # 更新counter内容
        else:
            logger.warning(f"[s2]data is empty,state{counter.valid_check()}")
            counter.set_state(-1)
            return counter  # 异常跳出
    # [收到zed信息][收到子站信息]获取子站索引，计算重叠索引（确保顺序）
    if counter.get_cnt_1() and counter.get_cnt_2():
        data: list[str] = counter.get_content_1()
        counter.set_content_1(cnt=[int(k) for k in data])
        logger.info(counter.get_content_1()) #t0218
        idx_list: list[list[int]] = []
        for data in counter.get_content_2():
            if data:
                try:
                    idx_list.append([int(k) for k in data])
                except ValueError:
                    logger.warning(f"[s2][int(k) for k in data][ValueError]{data}")
                    counter.set_state(-1)
                    return counter
            else:
                counter.set_state(-1)
                return counter
        # if counter.valid_check():  # 上一个异常没跳出去，这里跳出
        [temp_idx_0, temp_idx_list] = state2_calcu_overlap_index(idx_list_father=counter.get_content_1(),
                                                                     idx_list_son=idx_list)  # DONE:检查输入格式
        # [test]异常索引
        if temp_idx_0 == -1:
            temp_idx_0 = 1
            global_mark_error = 1
        else:
            global_mark_error = 0
            temp_idx_0 = max(temp_idx_0 - BaseConfig.INDEX_MOVE, 1)
        logger.info(f"match index, parent:{temp_idx_0}, son:{temp_idx_list}")
        counter.set_content_1(cnt=temp_idx_0)
        # [test]索引测试
        # counter.set_content_3(cnt=[temp_idx_0] * len(temp_idx_list))
        counter.set_content_3(cnt=temp_idx_0)
        # counter.set_content_3(cnt=temp_idx_list)
        temp_CMD = state2_data_to_cmd_ned(data=temp_idx_0)
        global_params.set_queue_tosend_data_to_global(queue_name=comm_thread_name_zed, data=temp_CMD)
        counter.mark["zed"]: bool = True

    # DONE:[索引计算完成]索引信息生成NED指令，按顺序向子站【分别】发送NED指令
    if counter.get_cnt_3():
        data: int = counter.get_content_3()
        try:
            send_to_all(f"idx\n{data}")  # 改为统一索引
        except Exception as e:
            logger.warning(f"[s2]{e}:send to sons failed")
            counter.set_state(-1)
            return counter
        counter.mark["son"]: bool = True
    # 异常处理
    if not valid_detect():
        counter.set_state(-1)
        return counter
    # [发送指令结束]切换到下一状态
    if counter.mark["zed"] and counter.mark["son"]:
        if counter.valid_check():
            logger.info("mode changed into 3")
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
            counter.next_state()  # 切换状态
    return counter


def state_3_main(counter: Task) -> Task:
    # 状态3数据位置安排：
    # 1号槽：zed数据段
    # 2号槽：时差列表
    # 3号槽：位置信息
    # [未收到zed信息]等待接收zed的数据信息
    global global_mark_error
    global freq_send
    if not counter.get_cnt_1():
        start_time = datetime.datetime.now()
        while True:
            if global_params.query_queue_data_exist(queue_name=comm_thread_name_zed)[0]:  # zed到达消息
                data: str = global_params.get_queue_gotten_data_from_global(queue_name=comm_thread_name_zed)
                if data.startswith("I:for toa"):  # 格式检验
                    counter.set_content_1(cnt=data)
                    # TODO:fft_memory
                    # data: list[str] = data.split('\n')
                    # do_fft_memory.do_data_save(recv_data=[f"findin{freq_send}"] + data[1:],
                    #                            dataName=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
                    # 发送信息
                    child_service.do_ope_on_child(child_service.fetch_child_single, False)
                    try:
                        send_to_all(counter.get_content_1())  # 广播消息
                    except Exception as e:
                        logger.warning(f"[s3]{e}:send to sons failed")
                        counter.set_state(-1)
                        return counter
                    break
            end_time = datetime.datetime.now()
            delta_time: datetime.timedelta = end_time - start_time
            # 超时case
            if delta_time.seconds > BaseConfig.WAIT_OVER_TIME:  # 1.5*BaseConfig.SET_DELAY_TIME:
                counter.set_state(-1)
                return counter  # 异常跳出
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
    # [未收到子站信息]等待接收子站时差信息（记录顺序）
    if not counter.get_cnt_2():
        data: list = []
        # 超时检测起点
        start_time: datetime = datetime.datetime.now()
        while not child_service.check_child_info():
            end_time: datetime = datetime.datetime.now()
            delta_time: datetime.timedelta = end_time - start_time
            # 超时case
            if delta_time.seconds > BaseConfig.WAIT_OVER_TIME:  # 1.5*BaseConfig.SET_DELAY_TIME:
                logger.warning("loop over time")
                counter.set_state(-1)
                return counter
        counter.set_content_3(cnt=list(child_service.check_child_info()))
        for ci in counter.get_content_3():
            temp: None = None
            if child_service.query_child_single(ci):
                temp: dict = child_service.fetch_child_single(ci)
                temp: Optional[str] = temp.get("info", None)
            while (not temp) or not temp.startswith("result"):
                time.sleep(BaseConfig.LOOP_WAIT_TIME)
                flag: bool = child_service.query_child_single(ci)
                if flag:
                    temp: dict = child_service.fetch_child_single(ci)
                    temp: Optional[str] = temp.get("info", None)
                    # temp: Optional[list[str]] = temp.split('\n') if temp else None
                end_time: datetime = datetime.datetime.now()
                delta_time: datetime.timedelta = end_time - start_time
                # 超时case
                if delta_time.seconds > BaseConfig.WAIT_OVER_TIME:  # 1.5*BaseConfig.SET_DELAY_TIME:
                    logger.warning("loop over time")
                    counter.set_state(-1)
                    return counter
            temp: list[str] = temp.split('\n')
            data.append(temp[1:])
        if data and counter.valid_check():
            # counter.set_content_3(cnt=list(child_service.check_child_info()))
            logger.info(f"[test][s3]d_list:{counter.get_content_3()}")
            counter.set_content_2(cnt=data)  # 更新counter内容
            counter.mark["son"]: bool = True
        else:
            logger.warning(f"[s3]data is empty,state{counter.valid_check()}")
            counter.set_state(-1)
            return counter
    # [收到子站信息]进行定位解算
    if counter.get_cnt_2():
        if global_mark_error == 0:
            data: list[str] = counter.get_content_2()
            d_list: list = counter.get_content_3()
            logger.info(f"test result:self {local_service.str2po(BaseConfig.host_address)}\n")
            for i in range(min(len(data), len(d_list))):
                logger.info(f"test result:{data[i]} from {d_list[i]['child_geo']}\n")
            # 测试临界区:
            # [B, L, H] = state3_tdoa_calcu(ci_list=counter.get_content_3(),diff_time_list=data)  # tdoa解算
            # counter.set_content_3([B, L, H])
            # print(L, B, H)  # TODO:计算结果出口
            # logger.info(f"test result:{data}")
            logger.info(f"===========================================================================")
        else:
            logger.info(f"test result: error data")
            d_list: list = counter.get_content_3()
            for i in range(len(d_list)):
                logger.info(f"from {d_list[i]['child_geo']}\n")
            logger.info(f"***************************************************************************")

        counter.mark["zed"]: bool = True
    # 异常处理
    if not valid_detect():
        counter.set_state(-1)
        return counter
    # [解算完成]切换到下一状态
    if counter.mark["zed"] and counter.mark["son"]:
        if counter.valid_check():
            logger.info("mode changed into 0")
            time.sleep(BaseConfig.LOOP_WAIT_TIME)
            counter.next_state()  # 切换状态
    return counter


def state_e_main(counter: Task) -> Task:
    # 异常状态处理
    logger.warning("mode arrive at -1")
    time.sleep(BaseConfig.LOOP_WAIT_TIME)
    # 子站状态位初始化，子站发送队列清空
    child_service.do_ope_on_child(child_service.invalid_mode_init_single)
    try:
        # 向子站：报错指令
        send_to_all(BaseConfig.INS_ERROR)  # 广播消息
        # 向子站：重启指令
        send_to_all(BaseConfig.INS_RESTART)  # 广播消息
    except Exception as e:
        logger.warning(f"[s-1]{e}:send to sons failed")
        counter.set_state(-1)
        time.sleep(BaseConfig.LOOP_WAIT_TIME)
        return counter
    # 清空zed发送队列
    global_params.get_queue_tosend_data_from_global(queue_name=comm_thread_name_zed, mode=False)
    # 重置zed异常状态
    global_params.set_valid_from_global(queue_name=comm_thread_name_zed, mark=True)
    time.sleep(BaseConfig.LOOP_WAIT_TIME)
    counter.restart_task()  # 重启状态
    logger.warning("mode changed into 0")
    return counter


# 其他功能函数
# 统一异常处理
def valid_detect() -> bool:
    # 主站异常处理
    all_flag: Optional[list[bool]] = child_service.do_ope_on_child(child_service.fetch_valid_single)
    if all_flag and not all(all_flag):
        logger.warning("status of sons is not right")
        return False
    # 子站数量检查
    if len(child_service.check_child_info()) < BaseConfig.MIN_STATION_NUM:
        logger.warning("num of son is not enough")
        return False
    # zed错误处理
    if not global_params.get_valid_from_global(queue_name=zed_service.get_global_var_name_from_zed()):
        logger.warning("status of zed is not right")
        return False
    return True


# 广播消息
def send_to_all(content: str) -> None:
    info: PureInfo = PureInfo(info={"info": content})
    child_service.do_ope_on_child(child_service.add_info_to_queue_single, info)
    child_service.do_ope_on_child(child_service.buffer_data_send_single)


# 将接收到的data信息转换成SET指令
def state1_data_to_cmd_set(data):
    # data 形式：[5800000000,536]
    freq = data[0]
    d_value = data[1]
    dtime = datetime.datetime.now(datetime.timezone.utc)
    dtime += datetime.timedelta(seconds=BaseConfig.SET_DELAY_TIME)
    temp_st = [dtime.hour, dtime.minute, dtime.second]
    if len(data) > 2:
        g_value = data[3]
    else:
        g_value = 71
    pass
    if data:
        try:
            temp = ZedOrderSET(start_time=temp_st, freq=freq, d_value=d_value,
                               gain_value=g_value)  # 此前获取消息中的参数信息，在此进行验证和指令转化
            return temp.rntcmd()
        except ValueError:
            logger.warning(f"{temp_st},{freq},{d_value},{g_value}")
    return


# 将接收到的data信息转换成NED指令
def state2_data_to_cmd_ned(data):
    temp = ZedOrderNED(idx=int(float(data)))  # 此前获取消息中的参数信息，在此进行验证和指令转化
    return temp.rntcmd()


# 计算重叠索引，按顺序返回
def state2_calcu_overlap_index(idx_list_father: list, idx_list_son: list[list]):
    res = local_service.f_calcu_overlap(idx_list_father, idx_list_son)
    if not res:
        return [1, [1] * len(idx_list_son)]
    return [res[0], res[1:]]


# TDOA定位解算
def state3_tdoa_calcu(ci_list, diff_time_list: list[float]):
    B_MASTER = local_service.str2po(BaseConfig.host_address)  # 获取主站GPS位置:[H,B(3),L(3)]高、纬、经
    geo_list = [B_MASTER]
    for ci in ci_list:
        geo_list.append(local_service.str2po(ci["child_geo"]))
    [res_B, res_L, res_H] = local_service.tdoa_main(geo_list, diff_time_list)
    # TODO:转换为能解析，并在地图上标注的格式
    return [res_B, res_L, res_H]


if __name__ == "__main__":
    # fft部分测试
    def readdata(path: str) -> list[str]:
        content = ""
        with open(path, 'r') as file:
            for line in file:
                content += line
        return content.split('\n')

    # import re
    # import numpy as np
    # from matplotlib import pyplot as plt
    # from scipy.signal import stft

    # data_list_i = []
    # data_list_q = []
    # v_freq = []
    # pattern = r'-?\d+'
    # with open(r"C:\Users\babab\Desktop\1-p.txt") as file:
    #     for line in file:
    #         # 找频点
    #         print(line)
    #         num_freq = re.search(r'findin\s*(-?\d+)', line)
    #         if num_freq:
    #             v_freq.append(num_freq.group(1))
    #         num_line = re.findall(r'(-?\d+),(-?\d+)', line)
    #         # print(num_line)
    #         # 找数据
    #         if num_line:
    #             for match in num_line:
    #                 before_comma, after_comma = map(int, match)
    #                 data_list_i.append(before_comma)
    #                 data_list_q.append(after_comma)
    # [data_i, data_q, _] = do_fft_memory.f_de_time_stamp(data_list_i, data_list_q)
    # np_i = np.array(data_i)
    # np_q = np.array(data_q)
    # np_sig = np_i + 1j * np_q
    # f, t_stft, Zxx = stft(np_sig, fs=int(v_freq[0]))
    # # 绘制STFT结果
    # plt.figure(figsize=(10, 6))
    # plt.pcolormesh(t_stft, f, np.abs(Zxx), shading='gouraud')
    # plt.title('STFT Magnitude')
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # plt.colorbar(label='Magnitude')
    # plt.show()
