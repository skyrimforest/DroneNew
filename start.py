import yaml
import subprocess
import sys
from pathlib import Path
import os
import socket

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RUNTIME_DIR = Path(".runtime")
RUNTIME_DIR.mkdir(exist_ok=True)
global_config={}

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def load_config(config_file="application.yaml"):
    """
    解析配置,存储在为字典
    """
    global global_config
    with open(config_file, "r", encoding="utf-8") as f:
        config=yaml.safe_load(f)
        global_config=config['config']
        # 使用新配置覆盖BaseConfig中的配置
        print(global_config)
    print("[Config] User Configuration Loaded successfully...")

def get_PC_info():
    """
    获取当前PC对应的信息
    """
    global global_config
    data={}
    # 本机名称
    HOST_NAME = socket.gethostname()
    # 自己的IP
    HOST_IP = get_host_ip()

    data["HostName"] = HOST_NAME
    data["HostIP"] = HOST_IP
    global_config['PC']=data
    print("[Config] PC Configuration Loaded successfully...")


def start_single_uvicorn(entry, host, port, name):
    global global_config

    print(f"[+] 启动模块: {name} -> http://{host}:{port}")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", entry,
        "--host", host,
        "--port", str(port),
        "--reload"
    ])
    with open(RUNTIME_DIR / f"pid_{name}.txt", "w") as f:
        f.write(str(process.pid))
    print(f"[Create] {entry} created successfully...")


def start_uvicorn():
    global global_config
    for name, settings in config.items():
        if settings.get("enable", False):
            start_single_uvicorn(
                entry=settings["entry"],
                host=settings.get("host", "127.0.0.1"),
                port=settings.get("port", 8000),
                name=name
            )
    print(f"[Create] All modules created successfully...")

def start_front():
    print(f"[Create] Frontend created successfully...")

def bootstrap(config_file="application.yaml"):
    """
    利用已有的global_config外加python对操作系统自身的读取能力,启动整个系统
    """
    # ---------- 读取配置 ----------
    print("[Bootstrap] Loading configuration...")
    load_config(config_file)
    get_PC_info()
    # ---------- 创建组件 ----------
    print("[Bootstrap] Scanning and creating components...")
    start_uvicorn()
    start_front()

    print("[Bootstrap] Bootstrap Finished successfully...")


if __name__ == "__main__":
    bootstrap()
