# [20250220] 用于控制站与zed间的tcp操作
import queue
import socket
import threading
import time
import datetime
from SkyLogger import get_logger

logger = get_logger("tcp_tools")


class TCPServer:
    def __init__(self, client_ip, client_port, reconnect_interval=3):
        # 连接参数
        self.client_ip = client_ip
        self.client_port = client_port
        self.reconnect_interval = reconnect_interval

        # 连接控制相关
        self.conn = None
        self.running = False
        self.lock = threading.Lock()

        # 数据队列
        self.send_queue = queue.Queue()
        self.recv_queue = queue.Queue()

    def start(self):
        """启动服务器"""
        self.running = True
        logger.info("[tcpserver:start][t0220]TCPServer started, waiting for connection...")
        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.connect((self.client_ip, self.client_port))
                    self.conn = s
                    logger.info(f"[tcpserver:start][t0220]Connected to {self.client_ip}:{self.client_port}")

                    # 启动收发线程
                    recv_thread = threading.Thread(target=self._recv_loop)
                    send_thread = threading.Thread(target=self._send_loop)

                    recv_thread.start()
                    send_thread.start()

                    # 等待线程结束
                    recv_thread.join()
                    send_thread.join()

            except (ConnectionRefusedError, TimeoutError) as e:
                logger.warning(f"[tcpserver:start][t0220]Connection failed: {e}, retrying in {self.reconnect_interval}s...")
                time.sleep(self.reconnect_interval)
            except Exception as e:
                logger.error(f"[tcpserver:start][t0220]Unexpected error: {e}")
                self.stop()

    def stop(self):
        """停止服务器"""
        self.running = False
        if self.conn:
            try:
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()
            except Exception as e:
                logger.warning(f"[tcpserver:stop][t0220]error: {e}")
        logger.info("[tcpserver:stop][t0220]Server stopped")

    def _recv_loop(self):
        """接收数据线程"""
        while self.running and self.conn:
            try:
                buffer = b''
                command = self.conn.recv(16)
                if not command:  # 连接关闭
                    raise ConnectionError("[tcpserver:recv][t0220]Connection closed by peer")
                buffer += command
                cmd_de = command.decode()
                if not (ord('A') <= ord(cmd_de[0]) <= ord('Z')):
                    continue
                data_length = int(cmd_de.split()[1])
                buffer += b"\n"
                for cnt in range(data_length):
                    data = self.conn.recv(1 * 1024)
                    buffer += data
                self.recv_queue.put(buffer.rstrip())
                # logger.info(f"{buffer.rstrip()}")

            except (ConnectionResetError, BrokenPipeError) as e:
                logger.error(f"[tcpserver:recv][t0220]Connection lost: {e}")
                self._reconnect()
                break
            except Exception as e:
                logger.error(f"[tcpserver:recv][t0220]Receive error: {e}")
                self._reconnect()
                break

    def _send_loop(self):
        """发送数据线程"""
        while self.running and self.conn:
            try:
                # 从队列获取待发送数据
                data = self.send_queue.get(timeout=1)
                # logger.info(f"[tcpserver:send][t0220]msg to be sent")
                with self.lock:
                    self.conn.sendall(data)
                    logger.info(f"[tcpserver:send][t0220]Sent message: {data}...")

            except queue.Empty:
                continue
            except (OSError, ConnectionError) as e:
                logger.error(f"[tcpserver:send][t0220]Send error: {e}")
                self._reconnect()
                break
            except Exception as e:
                logger.error(f"[tcpserver:send][t0220]Unexpected send error: {e}")
                continue

    def _reconnect(self):
        """执行重连操作"""
        logger.info("[tcpserver:reconnect][t0220]Attempting to reconnect...")
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
        self.conn = None

    def send_message(self, data):
        """外部调用发送消息"""
        self.send_queue.put(data)

    def get_message(self):
        """获取接收到的消息"""
        try:
            return self.recv_queue.get_nowait()
        except queue.Empty:
            return None