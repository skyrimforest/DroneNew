# 该文件用于与板卡建立tcp连接并传输数据
# 该文件作为一个简单的服务器端
import socket
import threading
import time
import csv


# 具体思路为对传输的数据进行关键字分割,之后就可以获取每条信息

# 获取socket
def get_server_socket():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8001))
        server_socket.listen(5)
        return server_socket
    except:
        return None


# 和服务器连接
def listen_to_client(server_socket, buffer_list):
    while True:
        try:
            conn, addr = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, buffer_list))
            client_handler.start()
        except Exception as e:
            print(e)


# 关闭
def close_socket(cli_socket):
    cli_socket.close()


def read_data():
    with open('1.txt', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        print(csv_reader.__next__())
        # for row in csv_reader:
        #     data.append(row[0])


# 服务函数
def handle_client(cli_socket, buffer):
    cnt = 0
    data = []
    f = open('4.txt', 'rb')
    while True:
        try:
            # 接收客户端发送的数据
            print("sending...")
            # cnt += 1
            while True:
                try:
                    command = f.read(16)
                    print(f"命令{command}")
                    if command.isspace():
                        print("2333")
                        time.sleep(2)
                        raise Exception
                    cli_socket.sendall(command)

                    data_len = int(command.split()[1])
                    print(data_len)
                    cnt = 0
                    while cnt < data_len:
                        data2sent = f.read(1024)
                        cnt += 1
                        cli_socket.sendall(data2sent)
                except Exception as e:
                    print(e)
                    f.seek(0)
                    break
        except ConnectionResetError:
            break
        # time.sleep(2)

    cli_socket.close()


if __name__ == '__main__':
    my_socket = get_server_socket()
    listen_to_client(my_socket, [])
    close_socket(my_socket)
