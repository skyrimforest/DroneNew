import os
import signal
from pathlib import Path

RUNTIME_DIR = Path(".runtime")

def stop_all():
    if not RUNTIME_DIR.exists():
        print("[-] 没有运行时信息，系统可能未启动。")
        return

    for pid_file in RUNTIME_DIR.glob("pid_*.txt"):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            print(f"[x] 已停止进程 {pid} ({pid_file.stem.replace('pid_', '')})")
        except ProcessLookupError:
            print(f"[!] 找不到进程 {pid}，可能已退出")
        except Exception as e:
            print(f"[!] 停止进程失败: {e}")
        finally:
            pid_file.unlink()

    RUNTIME_DIR.rmdir()

if __name__ == "__main__":
    stop_all()
