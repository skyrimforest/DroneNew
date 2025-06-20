'''
@Project ：pyfw01 
@File    ：drone_service.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/11/21 9:59 
'''
from geoMaster.BaseConfig.base_config import BaseConfig

def get_drone_data_child():
    return []

def get_drone_data_master():
    return []

def get_all_drone_info():
    res_list=[]
    # 从child获取无人机信息
    child_drone_list=get_drone_data_child()
    # 从master获取无人机信息 数据在DB内
    master_drone_list=get_drone_data_master()

    res_list+=child_drone_list
    res_list+=master_drone_list

    return res_list

# 获取无人机的数据
def get_drone_data():
    flag=False
    # # 获取最新文件 记录本次无人机数据
    # path_folder = BaseConfig.DB_PATH + '/DRONE_DATA/'
    # filename=path_folder+do_fft.f_find_latest_txt(path_folder)
    # if not check_new(filename):
    #     return {},flag
    #
    # flag=True
    # drone_info=drone_dao.get_drone_data_from_file(filename).split(' ')
    # drone_dao.insert_drone_data(drone_info)
    # # 获取总共检测次数
    # total_len=drone_dao.get_drone_data_len()
    # data={
    #     "drone_type":drone_info[0],
    #     "frequency":drone_info[1],
    #     "place":drone_info[2],
    #     "detect_time":drone_info[3],
    #     "total_len":total_len[0][0]
    # }
    # return data,flag

def get_drone_pic_url(drone_type):
    prefix=BaseConfig.DB_PATH + '/DRONE_PIC/'
    path=prefix+drone_type+".png"
    return path


# todo
def get_drone_from_child_single(ci):
    # child_ip = ci['child_ip']
    # child_port = ci['child_port']
    # child_url = "http://" + child_ip + ":" + child_port + child_api.API['frequency']
    # res = requests.post(child_url)
    # child_item = {
    #     "name": ci['uuid'],
    #     "data": json.loads(res.text)
    # }
    # logger.info(f"frequency got from {ci['uuid']}")
    return {}, False


# 从所有子节点获取drone值
# 返回值为字典类型的数组,记录每个子节点的新无人机信息
# 如果都没有更新 则返回false 如果存在更新 则返回true
# todo
def get_drone_from_child():
    global child_dict
    res_dicts = []
    flag = True
    for _, child in child_dict.items():
        data, temp_flag = get_drone_from_child_single(child)
        if temp_flag:
            res_dicts.append(data)
        else:
            flag = flag and temp_flag
    return res_dicts, flag