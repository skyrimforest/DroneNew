'''
@Project ：DroneContest
@File    ：spectrogram_service.py
@IDE     ：PyCharm
@Author  ：Skyrim
@Date    ：2025/7/1 23:04
'''
import asyncio
import matplotlib.pyplot as plt
import io, base64, json
# from geoMaster.utils.frequency.new_58 import draw_58
# from geoMaster.utils.frequency.new_24 import draw_24
from geoMaster.utils.frequency.just_draw import create_random_pic

# 引入日志
from geoMaster.SkyLogger import get_logger

logger = get_logger("spectrogram_service")


# todo 需要更换为实际的绘图逻辑


# async def spectrogram_24():
#     # 返回b64编码的图像
#     while True:
#         fig, img = draw_24()
#
#         buf = io.BytesIO()
#         plt.savefig(buf, format="png")
#         plt.close(fig)
#         img_base64 = base64.b64encode(buf.getvalue()).decode()
#
#         payload = json.dumps({"img": f"data:image/png;base64,{img_base64}"})
#         yield f"data: {payload}\n\n"
#
#         await asyncio.sleep(0.5)  # 控制推送频率
#
#
# async def spectrogram_58():
#     # 返回b64编码的图像
#     while True:
#         fig, img = draw_58()
#
#         buf = io.BytesIO()
#         plt.savefig(buf, format="png")
#         plt.close(fig)
#         img_base64 = base64.b64encode(buf.getvalue()).decode()
#
#         payload = json.dumps({"img": f"data:image/png;base64,{img_base64}"})
#         yield f"data: {payload}\n\n"
#
#         await asyncio.sleep(0.5)  # 控制推送频率


async def spectrogram_test():
    # 返回b64编码的图像
    while True:
        fig, ax = create_random_pic()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        img_base64 = base64.b64encode(buf.getvalue()).decode()
        payload = json.dumps({"img": f"data:image/png;base64,{img_base64}"})
        yield f"data: {payload}\n\n"

        await asyncio.sleep(0.5)  # 控制推送频率
