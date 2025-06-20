# 创建子进程运行脚本
import os
import signal
import subprocess
import time

from geoDisturber.SkyLogger import get_logger
# 信息传输类
from geoDisturber.schema.all_schema import CommandInfo
# 根路径
from geoDisturber.BaseConfig.base_config import BaseConfig
# yaml配置格式读取
import yaml

logger = get_logger("script_service")

# 管理运行的脚本进程
processList = {}

# 运行脚本
# command是脚本文件名称
# args是脚本参数
def get_script_name(ci: CommandInfo, dirName=BaseConfig.TARGET_SCRIPTS_PATH):
    script_target = BaseConfig.SCRIPTS_PATH + "/" + dirName + "/" + ci.pattern + "/" + ci.power + "/" + ci.command + ".pyc"
    return script_target


def run_script(ci: CommandInfo):
    script_target = get_script_name(ci)
    result = subprocess.run(['python', script_target], capture_output=True, text=True)
    if result.returncode != 0:
        logger.info("Error:", result)
    else:
        logger.info("Output:", result)


def get_script_process(ci: CommandInfo):
    script_target = get_script_name(ci)
    logger.info(f"{ci} has started...")
    arg_list = []
    for item in ci.arguments:
        res = item.items()
        for key, value in res:
            arg_list.append("--" + key)
            if type(value) is list:
                for v in value:
                    arg_list.append(str(v))
            if type(value) is int or type(value) is str:
                arg_list.append(str(value))
    command = ["python", script_target] + arg_list
    timestamp = str(time.time())[-12:]
    result = subprocess.Popen(command, start_new_session=True, )
    global processList
    uuid = timestamp
    script_info = {
        "timestamp": str(timestamp),
        "script": script_target,
        "command": ci.command
    }
    processList[uuid] = result
    return script_info


# 停止脚本
# 根据uuid停止脚本
def stop_script(uuid: str):
    global processList
    nameList = processList.keys()
    if uuid in nameList:
        os.kill(processList[uuid].pid, signal.SIGTERM)
        processList.pop(uuid)
        logger.info(f"{uuid} has stopped...")


# 根据配置文件获取全部的脚本信息
def get_script(config_file="config"):
    config_target = BaseConfig.SCRIPTS_PATH + "/" + config_file + ".yaml"
    with open(config_target, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for item in config['config']['patterns']:
        for command in item['pattern']['commands']:
            for idx, file in enumerate(command["command"]["files"]):
                command["command"]["files"][idx] = file[0:-3]
        #     item['pattern']['files'][idx] = file[0:-3]
    return config
