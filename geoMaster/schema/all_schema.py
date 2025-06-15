from pydantic import BaseModel
import threading
import queue


# 除下方字段 数据库中也存储id,time等字段
# 仅记录单个子节点的信息,uuid为本次事务
class ChildInfo(BaseModel):
    child_name: str  # 名称
    child_ip: str  # 网络地址
    child_port: str  # 服务端口号
    child_geo: str  # 地理位置,通过x_y表示 # 新格式为 HH_B1_B2_B3_L1_L2_L3 (HH、B3、L3带小数)


# 单纯的信息
class PureInfo(BaseModel):
    info: dict


class PureStr(BaseModel):
    info: str


class UserInfo(BaseModel):
    id: str
    nick_name: str
    icon: str


# 维护两个队列 作为发送缓冲区和接收缓冲区
class CommGlobalPara:
    def __init__(self,valid=True):
        self.lock = threading.Lock()
        self.msg_gotten = queue.Queue()
        self.msg_tosend = queue.Queue()
        self.valid = valid


class ZedOrderSET(BaseModel):
    start_time: list[int]
    freq: int = 5_840_000_000
    d_value: int
    gain_value: int = 71
    cmd2zed: str = None

    def isvalid(self):
        # TODO:异常提示形式
        value = self.start_time
        if len(value) == 0 or len(value) > 4:
            raise ValueError('len of <start_time> must be 1~4')
        if value[0] < 0 or value[0] >= 24:
            # raise ValueError('hour of <start_time> must be 0~23')
            self.start_time[0] = self.start_time[0] % 24
        value = self.freq
        if value <= 0 or value > 10e9:
            # raise ValueError('value of <freq> must in (0,10e9)')
            self.freq = int(float(5.8e9))
        value = self.d_value
        if value <= 0 or value > 2000:
            # raise ValueError('value of <d_value> must in (0,2000)')
            self.d_value = 133
        value = self.gain_value
        if value < 0 or value > 71:
            # raise ValueError('value of <gain_value> must in [0,71]')
            self.gain_value = 71
        return True

    def generate_cmd(self):
        if not self.cmd2zed:
            # para：start time
            para_start_time = []
            t_n = len(self.start_time)
            for i in range(4):
                if t_n <= i:
                    para_start_time.append('00')
                else:
                    para_start_time.append(f"{self.start_time[i]}".rjust(2, '0'))
            time_start = f"{para_start_time[0]}{para_start_time[1]}{para_start_time[2]}{para_start_time[3]}"
            message1 = ''.join(f"set t{time_start.rjust(11)}")
            # para:freq
            para_center_freq = self.freq
            message2 = ''.join(f"set f{str(para_center_freq).rjust(11)}")
            # para:D
            para_d_value = self.d_value
            message3 = ''.join(f"set d{str(para_d_value).rjust(11)}")
            # para:G
            para_gain_value = self.gain_value
            message4 = ''.join(f"set g{str(para_gain_value).rjust(11)}")
            self.cmd2zed = ''.join([message1, message2, message3, message4])

    def rntcmd(self) -> str:
        self.generate_cmd()
        return self.cmd2zed


class ZedOrderNED(BaseModel):
    idx: int = 1
    cmd2zed: str = None

    def isvalid(self):
        if self.idx <= 0 or self.idx > 10485765 - 10240:
            # raise ValueError('value of <freq> must in (0,10485765 - 10240)')
            self.idx = 1
        else:
            return True

    def rntcmd(self) -> str:
        self.generate_cmd()
        return self.cmd2zed

    def generate_cmd(self):
        if not self.cmd2zed:
            para_time_stamp = self.idx
            self.cmd2zed = ''.join(f"ned t{str(para_time_stamp).rjust(11)}")


class Task:
    # DONE:信息同步
    # state:状态计数器
    #   功能包含：计数加一、计数设置、有效性检查
    # mark:状态内操作完成标识
    #   状态切换时自动置零
    # content1/2/3:3个数据槽位，用于同步
    #   状态切换时自动置零
    #   功能包含：写入、读取、清零
    # cnt1/2/3:数据槽位计数器，用于判断
    #   状态切换时自动置零，写入时自动加一
    #   功能包含：写入、读取、清零
    # __max_state:最大状态数
    # __lock：线程锁，内部函数获取
    # __condition：条件锁，内部函数获取
    def __init__(self, name=None, loop_max_num=3, init_num=0):
        self.name = name
        self.state = init_num
        self.__max_state = loop_max_num
        self.__lock = threading.Lock()
        self.__condition = threading.Condition()
        self.mark = {"zed": False, "son": False}
        self.content1 = []
        self.cnt1 = 0
        self.content2 = []
        self.cnt2 = 0
        self.content3 = []
        self.cnt3 = 0

    # 工作状态
    def next_state(self):
        if self.valid_check():
            with self.__lock:
                self.state += 1
                self.state %= self.__max_state
                for key in self.mark:
                    self.mark[key] = False
        self.new_cnt()

    def get_state(self):
        with self.__lock:
            return self.state

    def set_state(self, mode):
        with self.__lock:
            self.state = mode
            for key in self.mark:
                self.mark[key] = False

    def restart_task(self):
        self.set_state(0)
        self.new_cnt()

    def valid_check(self) -> bool:
        with self.__lock:
            return 0 <= self.state < self.__max_state

    def get_condition(self):
        return self.__condition

    # 存储内容
    def new_cnt(self):
        self.new_cnt1()
        self.new_cnt2()
        self.new_cnt3()

    def new_cnt1(self):
        with self.__lock:
            self.cnt1 = 0
            self.content1 = []

    def new_cnt2(self):
        with self.__lock:
            self.cnt2 = 0
            self.content2 = []

    def new_cnt3(self):
        with self.__lock:
            self.cnt3 = 0
            self.content3 = []

    def set_content_1(self, cnt):
        with self.__lock:
            if cnt is not None:
                self.cnt1 += 1
                self.content1 = cnt

    def get_content_1(self):
        with self.__lock:
            return self.content1

    def get_cnt_1(self):
        with self.__lock:
            return self.cnt1

    def set_content_2(self, cnt):
        with self.__lock:
            if cnt is not None:
                self.cnt2 += 1
                self.content2 = cnt

    def get_content_2(self):
        with self.__lock:
            return self.content2

    def get_cnt_2(self):
        with self.__lock:
            return self.cnt2

    def set_content_3(self, cnt):
        with self.__lock:
            if cnt is not None:
                self.cnt3 += 1
                self.content3 = cnt

    def get_content_3(self):
        with self.__lock:
            return self.content3

    def get_cnt_3(self):
        with self.__lock:
            return self.cnt3


if __name__ == '__main__':
    a = ZedOrderSET(start_time=[11, 26, 50], freq=5_840_000_000, d_value=536, gain_value=62)
    try:
        a.isvalid()
        print(a.rntcmd())
    except ValueError as e:
        print(f"error:{e},retry plz.")
    b = ZedOrderNED(idx=65534)
    try:
        b.isvalid()
        print(b.rntcmd())
    except ValueError as e:
        print(f"error:{e},retry plz.")
