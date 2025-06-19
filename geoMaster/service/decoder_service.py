'''
@Project ：DroneContest 
@File    ：decoder_service.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/19 20:57 
'''

from geoMaster.utils import decoder_util
# 引入日志
from geoMaster.SkyLogger import get_logger
import geoMaster.BaseConfig as BaseConfig

logger = get_logger("decoder_service")

def do_decode(file_name):
    return decoder_util.decoder_offline(file_name)

def get_input_info(path):
    return decoder_util.get_sample_file(path)


if __name__ == '__main__':
    res=get_input_info(BaseConfig.DECODER_PATH)
    print(res)