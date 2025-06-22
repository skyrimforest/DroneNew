import yaml
import subprocess
import sys
from pathlib import Path
import os
import socket
from registry.scanner import scan_and_register_components
from registry.factory import create_component_by_id
import json
from datetime import datetime
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
RUNTIME_DIR = Path(".runtime")
RUNTIME_DIR.mkdir(exist_ok=True)
global_config = {}
package_list = []


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

def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def capture_initial_output(process, name, max_lines=10):
    lines = []
    for _ in range(max_lines):
        line = process.stdout.readline()
        if not line:
            break
        decoded = line.decode(errors="ignore").strip()
        clean_line = strip_ansi_codes(decoded)
        lines.append(clean_line)
    print(f"\n[Init Output] {name} 启动信息:")
    for l in lines:
        print(f"[{name}] {l}")
    return lines


def extract_urls_from_lines(lines):
    """
    从字符串列表中提取所有 URL。

    :param lines: List[str] - 每个元素是日志或输出中的一行
    :return: List[str] - 提取出的所有 URL（不重复）
    """
    url_pattern = re.compile(
        r'https?://[^\s"\']+|//[^\s"\']+'  # 匹配 http/https 或协议相对路径
    )

    urls = []
    for line in lines:
        matches = url_pattern.findall(line)
        urls.extend(matches)

    # 可选：去重 & 排序
    return sorted(set(urls))

def write_process_metadata(name, pid, meta: dict):
    metadata = {
        "pid": pid,
        "name": name,
        "start_time": datetime.now().isoformat(),
        **meta  # 例如 type, cwd, command 等
    }
    with open(RUNTIME_DIR / f"pid_{name}.txt", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def load_config(config_file="application.yaml"):
    """
    解析配置,存储在为字典
    """
    global global_config, package_list
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        global_config = config['config']
        for component in global_config['modules'].keys():
            package_list.append(component)
    print("[Config] User Configuration Loaded successfully...")


def get_PC_info():
    """
    获取当前PC对应的信息
    """
    global global_config
    data = {}
    # 本机名称
    HOST_NAME = socket.gethostname()
    # 自己的IP
    HOST_IP = get_host_ip()
    data["HostName"] = HOST_NAME
    data["HostIP"] = HOST_IP
    global_config['PC'] = data
    print("[Config] PC Configuration Loaded successfully...")


def scan_and_register():
    global package_list
    for package in package_list:
        scan_and_register_components(package)


def construct_baseconfig():
    global global_config
    package_baseconfig = []
    for package in package_list:
        try:
            data = {
                "module_name": package,
                "config": create_component_by_id(package + ".BaseConfig")
            }
            package_baseconfig.append(data)
        except ValueError as e:
            print(f"[Construct] 创建时出现值错误: {e}")  # 打印模块对象，而不是字符串

    # 遍历 global_config 中的所有字段，分别更新两个配置类中对应字段
    for config in package_baseconfig:
        for key, value in global_config['modules'][config['module_name']].items():
            if hasattr(config['config'], key):
                setattr(config['config'], key, value)

    print("[Construct] ✅ BaseConfig fields updated with global_config.")


def start_single_uvicorn(entry, host, port, name=None):
    print(f"[Create] [+] 启动模块: {name} -> http://{host}:{port}")

    cmd = [
        "uvicorn",
        entry,
        "--host", host,
        "--port", str(port),
        "--reload"
    ]
    process_name = f"[{name}]" if name else ""
    print(f"{process_name} ➤ Running command: {' '.join(cmd)}")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # 捕获前几行输出
    output_lines = capture_initial_output(process, name)

    # 写入元信息
    write_process_metadata(
        name=name,
        pid=process.pid,
        meta={
            "type": "uvicorn",
            "entry": entry,
            "host": host,
            "port": port,
            "command": " ".join(cmd),
            "output_preview": output_lines
        }
    )

    print(f"[Create] {entry} created successfully (PID: {process.pid})")


def start_uvicorn():
    global global_config

    for name, settings in global_config.items():
        if settings.get("enable", False):
            entry = settings["entry"]
            host = settings.get("host", "127.0.0.1")
            port = settings.get("port", 8000)

            print(f"[Create] Launching {name} at {host}:{port} -> {entry}")

            start_single_uvicorn(
                entry=entry,
                host=host,
                port=port,
                name=name
            )

    print(f"[Create] ✅ All uvicorn modules started successfully.")

def start_front():
    global global_config,ROOT_DIR

    front_config = global_config.get('front', {})
    print(f"[Create] [+] 启动前端模块: {front_config.get('name')}")

    command=["npm", "run", "dev"]
    # 启动前端开发服务（如 vite、vue-cli）
    process = subprocess.Popen(
        command,
        cwd=ROOT_DIR+f"/{front_config.get('name')}",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True
    )

    res=capture_initial_output(process, front_config.get('name'), max_lines=10)
    extract_urls_from_lines(res)
    print(res)
    write_process_metadata(
        name=front_config.get('name'),
        pid=process.pid,
        meta={
            "type": "vue",
            "cwd": ROOT_DIR+f"/{front_config.get('name')}",
            "command": command
        }
    )

    print(f"[Create] 前端模块 {front_config.get('name')} 启动成功...")
    return res

def bootstrap(config_file="application.yaml"):
    """
    利用已有的global_config外加python对操作系统自身的读取能力,启动整个系统
    """
    # ---------- 读取配置 ----------
    print("[Bootstrap] Loading configuration...")
    load_config(config_file)
    get_PC_info()

    # ---------- 扫描包 ----------
    print("[Bootstrap] Scan package and construct components...")
    scan_and_register()
    construct_baseconfig()

    # ---------- 创建组件 ----------
    print("[Bootstrap] Scanning and starting components...")
    start_uvicorn()
    start_front()

    print("[Bootstrap] Bootstrap Finished successfully...")


if __name__ == "__main__":
    bootstrap()
