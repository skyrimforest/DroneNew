# 系统运行后,使用该脚本开始网络测试
# 该网络测试会触发一个后台进程向/script发送post请求

import requests

if __name__ == '__main__':
    data={
        "command": "mynettest",
        "arguments": [{"end":20},{"numbers":[30,40,50]}],
        "pattern": "/pattern01",
        "power": ""
    }
    res=requests.post("http://127.0.0.1:10002/script/runscript", json=data)
    print(res.text)





