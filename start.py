import yaml
import subprocess
import sys
from pathlib import Path

RUNTIME_DIR = Path(".runtime")
RUNTIME_DIR.mkdir(exist_ok=True)

def load_config():
    with open("application.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def start_uvicorn(entry, host, port, name):
    print(f"[+] 启动模块: {name} -> http://{host}:{port}")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", entry,
        "--host", host,
        "--port", str(port),
        "--reload"
    ])
    with open(RUNTIME_DIR / f"pid_{name}.txt", "w") as f:
        f.write(str(process.pid))

def main():
    config = load_config()
    for name, settings in config.items():
        if settings.get("enable", False):
            start_uvicorn(
                entry=settings["entry"],
                host=settings.get("host", "127.0.0.1"),
                port=settings.get("port", 8000),
                name=name
            )

if __name__ == "__main__":
    main()
