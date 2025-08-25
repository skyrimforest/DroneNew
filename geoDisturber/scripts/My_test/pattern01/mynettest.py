# 测试脚本,睡眠n秒

import argparse
import os
import time
import requests

def parse_args():
    parser = argparse.ArgumentParser(description="Run Test Script")
    parser.add_argument(
        "--end", type=int, default="100", help="The End Number."
    )
    parser.add_argument(
        "--numbers", type=int,nargs="+", default=[], help="The Sum Number."
    )
    return parser.parse_args()

# 具体脚本的功能
def function_script(arg):
    total_time=sum(arg.numbers)
    if total_time==0:
        total_time=arg.end

    data = {
        "command": os.getpid(),
        "arguments": [""],
        "pattern": "",
        "power": "",
    }

    for i in range(0,total_time):
        time.sleep(1)
        requests.post("http://127.0.0.1:10002/script/",json=data)

args=parse_args()
print(args)
function_script(args)
