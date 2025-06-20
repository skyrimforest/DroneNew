# 主站的控制链路，负责与子站和zed交互
import time

from geoMaster.BaseConfig.base_config import BaseConfig
from geoMaster.schema.all_schema import CommGlobalPara, ChildInfo
from geoMaster.service import child_service, zed_service, state_service

from geoMaster.utils import global_params
from geoMaster.SkyLogger import get_logger
import threading
import csv
from geoMaster.dao import drone_dao

logger = get_logger("work_service")
last_file_name = None


# 工作循环主线程
def run_main_work_loop():
    # zed线程比较固定，因此直接固定全局变量启动
    client_thread1 = threading.Thread(target=zed_service.communicate_loop_to_zed)
    client_thread1.daemon = True
    client_thread1.start()
    # 控制线程
    client_thread2 = threading.Thread(target=state_service.control_loop)
    client_thread2.daemon = True
    client_thread2.start()
    while True:
        if not client_thread1.is_alive():
            client_thread1 = threading.Thread(target=zed_service.communicate_loop_to_zed)
            client_thread1.daemon = True
            client_thread1.start()
            logger.warning("thread zed reconnect")
        if not client_thread2.is_alive():
            client_thread2 = threading.Thread(target=state_service.control_loop)
            client_thread2.daemon = True
            client_thread2.start()
            logger.warning("thread son reconnect")
        time.sleep(10*BaseConfig.LOOP_WAIT_TIME)
        # logger.info("[test]work thread is online...")


def run_work_thread():
    work_thread = threading.Thread(target=run_main_work_loop)
    work_thread.daemon = True
    work_thread.start()
    logger.info("work Thread Started, do work...")
    return work_thread


if __name__ == '__main__':
    ''' 测试坐标
    3300_25_44_6_123_28_4
    4660.609_25_43_33.8905_123_29_33.7145
    1679.935_25_44_20.5502_123_26_34.2338
    5424.456_25_43_21.9411_123_27_4.7005
    915.641_25_44_32.5223_123_29_3.3511
    6907.435_25_41_10.6773_123_22_17.0189
    '''
    test_ci = ChildInfo(
        child_name="fallen-child01",
        child_ip="localhost",
        child_port="10001",
        child_geo="3300_25_44_6_123_28_4")
    test_ci2 = ChildInfo(
        child_name="fallen-child02",
        child_ip="localhost",
        child_port="10000",
        child_geo="4660.609_25_43_33.8905_123_29_33.7145")
    test_ci3 = ChildInfo(
        child_name="fallen-child03",
        child_ip="localhost",
        child_port="10001",
        child_geo="1679.935_25_44_20.5502_123_26_34.2338")
    test_ci4 = ChildInfo(
        child_name="fallen-child04",
        child_ip="localhost",
        child_port="10000",
        child_geo="5424.456_25_43_21.9411_123_27_4.7005")
    test_ci5 = ChildInfo(
        child_name="fallen-child05",
        child_ip="localhost",
        child_port="10001",
        child_geo="915.641_25_44_32.5223_123_29_3.3511")

    child_service.child_register(test_ci)
    child_service.child_register(test_ci2)
    child_service.child_register(test_ci3)
    child_service.child_register(test_ci4)
    child_service.child_register(test_ci5)
    p = [1495.75785303, -1027.04133802, -2546.75341576, 2590.61887237]
    ci_list = child_service.get_child_info()
    # [h, b, l] = state3_tdoa_calcu(ci_list, p)
    # print(h, b, l)
