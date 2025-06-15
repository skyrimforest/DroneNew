
这个项目用于管理ubuntu下脚本运行的
主体使用fastapi开发,可以使用脚本指定ip与端口
默认ip为本机ip,端口为10002
使用方法:
# 指定端口号为9000运行
python main.py --port 9000


部署主要注意事项：
1.为了运行gnuradio脚本，需要准备好安装有gnuradio库的python虚拟环境。
2.若按照组内安装gnuradio的方法，则在激活了该虚拟环境后，需要使用conda安装fastapi、PyYAML等库。
安装脚本：
conda install PyYAML
conda install fastapi
即可。
3.注意到scripts文件夹中有两个脚本组，也就是FW_test与My_test，对应两个yaml文件config.yaml与config_test.yaml
这两个yaml文件是用于配置脚本信息的，两个文件格式类似，文件内创建了patterns数组，每个数组都有一个pattern项，
其内部可以指定文件夹名称dirname、脚本名称name、功率power与具体的指令文件commands，因为配置信息的不同，
内部还会指定不同的config。这部分有问题可以直接滴滴我。
4.系统想要运行直接运行main.py文件即可，注意需要激活上面配置好的虚拟环境
运行脚本：
python main.py
此时命令行内如果打印INFO日志信息则启动成功。
5.系统test文件夹内配置了两个测试文件，分别管理一个脚本的开启与关闭。
脚本的运行信息长这样：
data={
        "command": "mynettest",
        "arguments": [{"end":20},{"numbers":[30,40,50]}],
        "pattern": "/pattern01",
        "power": ""
    }
可以写一个gnuradio的脚本信息看看是否能够正常运行。（不过需要修改系统的多个部分，可以直接滴滴咨询我修改方法，毕竟我的测试脚本和gnu脚本不在一个文件夹内）


