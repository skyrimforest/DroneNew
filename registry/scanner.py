'''
@Project ：tiangong 
@File    ：scanner.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/5/31 0:38 
'''
import importlib
import pkgutil

import yaml
import os
from registry import component_registry

def load_config(config_path: str):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    if "config" not in raw_config:
        raise ValueError("Missing 'config' section in configuration.")

    sky_config = raw_config["config"]

    component_registry['config'] = sky_config

def scan_and_register_components(package_name):
    """
    自动导入并触发装饰器注册
    """
    # 动态导入指定名称的模块
    try:
        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        print(f"[Scan] 扫描时出现模块错误: {e}")  # 打印模块对象，而不是字符串
    except Exception as e:
        print(f"[Scan] 扫描时出现错误: {e}")  # 打印模块对象，而不是字符串
