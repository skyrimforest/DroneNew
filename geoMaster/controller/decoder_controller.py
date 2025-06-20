'''
@Project ：DroneContest 
@File    ：decoder_controller.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2025/6/19 20:57 
'''
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

import geoMaster.BaseConfig as BaseConfig
from geoMaster.SkyLogger import get_logger
from geoMaster.service import decoder_service
from geoMaster.schema.all_schema import PureInfo

router = APIRouter(
    prefix="/decode",
    tags=["ai"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("decode")

# 调用解码器进行处理
@router.post("/dodecode")
async def drone_decoder(someinfo: PureInfo):
    data_packet = someinfo.info
    print(data_packet)
    filename = data_packet['filename']
    res=decoder_service.do_decode(filename)
    print(res)
    return {
        "success": True,
        "decode": res
    }

# 获取采集到的文件的信息
@router.get("/getpacketinfo")
async def sample_info():
    res=decoder_service.get_input_info(BaseConfig.DECODER_PATH)
    return {
        "success": True,
        "filelist": res
    }




