# 该文件用于与板卡建立tcp连接并传输数据
# 该文件作为一个简单的客户端
import socket

# 具体思路为对传输的数据进行关键字分割,之后就可以获取每条信息

# 获取socket
def get_client_socket():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return client_socket
    except:
        return None

# 和服务器连接
def connect_to_server(cli_socket,server_address):
    try:
        cli_socket.connect(server_address)
        return {"success":True}
    except:
        return {"success":False}

# 获取信息,使用了较为复杂的协议,不采用这版
def get_server_info(cli_socket,info="start"):
    try:
        cli_socket.sendall(info.encode())

        # 先接收4个字节长度(int型,代表消息长度)
        len_bytes=cli_socket.recv(4)
        info_len=int.from_bytes(len_bytes,byteorder='big')

        # 再获取真的消息
        data_bytes=cli_socket.recv(info_len)
        real_data=data_bytes.decode()

        print(real_data)
        return {"success":True,
                "data":real_data}
    except:
        return {"success":False}

# 获取信息,简单地固定了缓冲区大小为2048
def get_server_info_and_cut(cli_socket,buffer,info="start",):
    try:
        cli_socket.send(info.encode())

        # 获取一整段消息后做切分
        data_bytes=cli_socket.recv(2048)
        buffer.clear()
        buffer.append(data_bytes.decode())
        # real_data=data_bytes.decode()
        # data_list=real_data.split('@')
        # print(buffer)
        # cli_socket.close()
        return {"success":True,
                "data":buffer}
    except Exception as e:
        print(e)
        cli_socket.close()
        return {"success":False}

# 关闭
def close_socket(cli_socket):
    cli_socket.close()


if __name__ == '__main__':
    my_socket = get_client_socket()
    if my_socket:
        connect_to_server(my_socket,("127.0.0.1",8001))
        get_server_info_and_cut(my_socket)
        close_socket(my_socket)