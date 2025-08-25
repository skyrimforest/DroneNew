# 测试脚本,睡眠n秒

import argparse
import time

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
    print(f"total_time is {total_time}")
    for i in range(0,total_time):
        time.sleep(1)
        print(f"{i+1} slept")

if __name__ == '__main__':
    args=parse_args()
    print(args)
    function_script(args)
