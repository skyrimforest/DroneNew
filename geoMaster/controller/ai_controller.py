'''
@Project ：DroneContest 
@File    ：ai_controller.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/15 10:28 
'''

from fastapi import APIRouter
from geoMaster.SkyLogger import get_logger
from geoMaster.service import ai_service
from geoMaster.schema.all_schema import PureInfo

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("ai")


# 测试组件
@router.post("/")
async def test_ai():
    return {"ai_api_status": "ok"}


# 调用ai进行推理
@router.post("/aipredict")
async def heart_beat(someinfo: PureInfo):
    data_packet = someinfo.info
    data = data_packet['data']
    ai_service.ai_predict(data)
    image_url = ""
    return {
        "success": True,
        "url": image_url
    }
