# 测试脚本,输出1-n

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run Test Script")
    parser.add_argument(
        "--end", type=int, default="100", help="The End Number."
    )
    return parser.parse_args()

# 具体脚本的功能
def function_script(n):
    for i in range(0,n):
        print(f"{i+1} ",end="")

if __name__ == '__main__':
    args=parse_args()
    function_script(args.end)
