from sympy import false

from geoMaster.utils import ai_util
# 引入日志
from geoMaster.SkyLogger import get_logger
import geoMaster.BaseConfig as BaseConfig

logger = get_logger("ai_service")
# 存储临时文件路径的映射
temp_file_map = {}

def ai_predict(file_name):
    file_path=BaseConfig.BIN_PATH+'/'+file_name
    res=ai_util.ai_predict(file_path)
    pic_name = res['filename'].split('/')[-1]
    temp_file_map[pic_name]=res['filename']

    res['filename']=pic_name
    res['loading']=false
    res['url']=""
    return res

def get_input_info(path):
    return  ai_util.get_input_info(path)

def get_pic_path(pic_name):
    return temp_file_map[pic_name]

