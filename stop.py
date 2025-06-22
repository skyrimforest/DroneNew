import os
import json
import signal
from pathlib import Path

RUNTIME_DIR = Path(".runtime")

def stop_process_by_name(name: str):
    pid_file = RUNTIME_DIR / f"pid_{name}.txt"
    if not pid_file.exists():
        print(f"[Stop] ✖️ PID 文件不存在: {pid_file}")
        return

    try:
        with open(pid_file, "r", encoding="utf-8") as f:
            info = json.load(f)
            pid = info["pid"]

        print(f"[Stop] 尝试关闭模块 {name}（PID: {pid}）...")

        # 终止进程
        os.kill(pid, signal.SIGTERM)  # Windows/macOS/Linux 都支持
        print(f"[Stop] ✅ 模块 {name} 已关闭。")

        # 删除 PID 文件
        pid_file.unlink()

    except ProcessLookupError:
        print(f"[Stop] ⚠️ 进程 PID {pid} 不存在，可能已退出。")
        pid_file.unlink()

    except Exception as e:
        print(f"[Stop] ❌ 关闭模块 {name} 时出错: {e}")

