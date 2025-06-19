#!/usr/bin/env python3
"""
live_spectrogram.py
实时滚动显示 GNU Radio 通过 ZMQ PUB Sink 推送的 4096-float 频谱帧
• PUB Sink 请接在 Log10“之前”（线性功率），Vector Len = 4096
• 允许一条 ZMQ 消息中携带多帧 (N × 4096)
"""

import zmq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess, os, time, sys          # ← 新增 (放在其他 import 前)

# 启动 GRC 生成的 flowgraph（完整路径自己改）
gr_proc = subprocess.Popen([sys.executable, "/home/uhd/gps-sdr-sim/123/D24.py"])

# 等 IPC 文件出现（最多等 2 秒）
for _ in range(40):
    if os.path.exists("/tmp/fft.ipc"):
        break
    time.sleep(0.05)



IPC_ADDR  = "ipc:///tmp/fft.ipc"   # 与 GRC 中 PUB Sink 完全一致
VEC_LEN   = 3072                  # 一帧的点数
N_KEEP    = 2000                  # X 轴保留最近多少帧
FPS_LIMIT = 30                    # matplotlib 刷新上限 (fps)
# ZMQ SUB 端
ctx  = zmq.Context()
sock = ctx.socket(zmq.SUB)
sock.connect(IPC_ADDR)
sock.setsockopt(zmq.SUBSCRIBE, b"")
ring = np.zeros((N_KEEP, VEC_LEN), np.float32)
write_idx = 0

# matplotlib 画布
plt.figure("Live Spectrogram")
ax = plt.gca()
im = ax.imshow(np.zeros((VEC_LEN, N_KEEP), np.uint8),
               aspect="auto", origin="lower", vmin=0, vmax=255)
ax.set_xlabel("Time (frames)")
ax.set_ylabel("FFT bin")
plt.tight_layout()

# 更新函数 
def update(_):
    global write_idx
    got = False

    # 1) 把 ZMQ 缓冲区里的所有消息一次读光
    while True:
        try:
            msg = sock.recv(flags=zmq.NOBLOCK)
        except zmq.Again:
            break
        data = np.frombuffer(msg, np.float32)
        if data.size % VEC_LEN:          # ★ 非整数帧直接丢
            continue
        n_frames = data.size // VEC_LEN
        for k in range(n_frames):
            frame = data[k*VEC_LEN:(k+1)*VEC_LEN]
            ring[write_idx % N_KEEP] = frame
            write_idx += 1
        got = True

    if not got:               # 没有新帧就保持上一幅
        return im

    # 2) 取最近 N_KEEP 帧 → 转 dB → 归一化
    idx  = np.arange(write_idx - N_KEEP, write_idx) % N_KEEP
    spec = ring[idx]                              # shape (N_KEEP, 4096)
    spec_db = 20*np.log10(spec + 1e-12)           # ★ 数据已是线性功率!

    #   自适应 80 dB 动态窗，避免全黑 / 全紫
    db_max  = np.nanmax(spec_db)
    db_min  = db_max - 80.0
    spec_norm = np.clip((spec_db - db_min)/80.0, 0, 1)
    img = (spec_norm*255).astype(np.uint8)        # uint8 灰度

    # 3) 更新画面
    im.set_data(img.T)              # 频率纵轴 / 时间横轴
    ax.set_xlim(0, img.shape[0])    # X = N_KEEP
    ax.set_ylim(0, img.shape[1])    # Y = 4096
    
    return im
ani = animation.FuncAnimation(plt.gcf(), update,
                              interval=1000/FPS_LIMIT, blit=False)

print("Running…  关闭窗口或 Ctrl-C 退出")
plt.show()
gr_proc.terminate()        # 关闭流图子进程
