'''
@Project ：DroneContest 
@File    ：ai_controller.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/15 10:28 
'''

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from geoMaster.BaseConfig.base_config import BaseConfig
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
async def ai_infer(someinfo: PureInfo):
    data_packet = someinfo.info
    print(data_packet)
    filename = data_packet['filename']
    res=ai_service.ai_predict(filename)
    print(res)
    return {
        "success": True,
        "infer": res
    }

# 获取采集到的文件的信息
@router.get("/getbininfo")
async def sample_info():
    res=ai_service.get_input_info(BaseConfig.BIN_PATH)
    return {
        "success": True,
        "filelist": res
    }


# 获取图片
@router.get("/getpic/{image_name}")
async def pic_info(image_name:str):
    # 从映射中获取临时文件路径
    if image_name not in ai_service.temp_file_map:
        raise HTTPException(status_code=404, detail="Image not found")

    # 返回文件响应
    return FileResponse(ai_service.get_pic_path(image_name))