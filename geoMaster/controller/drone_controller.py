'''
@Project ：pyfw01 
@File    ：drone_controller.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/11/21 9:59 
'''
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse

from geoMaster.SkyLogger import get_logger
from geoMaster.service import zed_service
router = APIRouter(
    prefix="/drone",
    tags=["drone"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("drone")

# 给出无人机示意图
@router.get("/drone/{drone_type}")
async def show_drone(drone_type):
    path = zed_service.get_drone_pic_url(drone_type)
    return FileResponse(path, media_type="image/jpeg")

# 对无人机信息进行详细查询
@router.get("/drone")
async def show_drone():
    pass