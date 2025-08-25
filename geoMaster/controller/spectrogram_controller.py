'''
@Project ：DroneContest 
@File    ：spectrogram_controller.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/7/1 23:04 
'''

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse

from geoMaster.SkyLogger import get_logger
from geoMaster.service import spectrogram_service

router = APIRouter(
    prefix="/spect",
    tags=["spect"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("spectrogram")


# 绘制傅里叶图,总共有两种spectrogram24和spectrogram58
@router.get("/getpic/{image_name}")
async def get_spectrogram(image_name: str):
    # 从映射中获取临时文件路径
    if image_name not in spectrogram_service.temp_file_map:
        raise HTTPException(status_code=404, detail="Image not found")
    output = spectrogram_service.get_current_pic(image_name)
    # 返回文件响应
    return Response(output, mimetype='image/png')


# @router.get("/start24")
# async def spect_sse_start_24():
#     return StreamingResponse(spectrogram_service.spectrogram_24(), media_type="text/event-stream")
#
#
# @router.get("/start58")
# async def spect_sse_start_58():
#     return StreamingResponse(spectrogram_service.spectrogram_58(), media_type="text/event-stream")


@router.get("/start_test")
async def spect_sse_start_test():
    return StreamingResponse(spectrogram_service.spectrogram_test(), media_type="text/event-stream")

