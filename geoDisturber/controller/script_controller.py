import datetime

from geoDisturber.BaseConfig.base_config import BaseConfig
from geoDisturber.SkyLogger import get_logger
from fastapi import APIRouter
from geoDisturber.schema.all_schema import CommandInfo, ScriptInfo
from geoDisturber.service import script_service

router = APIRouter(
    prefix="/script",
    tags=["script"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("script")


# 测试组件
@router.post("/")
async def test_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

# 查询组件在线
@router.post("/heartbeat")
async def heart_beat():
    timestamp = datetime.datetime.now()
    return {"success": True, "timestamp": timestamp}

# 运行脚本
@router.post("/runscript")
async def run_script(ci: CommandInfo):
    script_info = script_service.get_script_process(ci)
    return {
        "data": script_info
    }


# 停止运行脚本
@router.post("/stopscript")
async def stop_script(si: ScriptInfo):
    script_service.stop_script(si.uuid)
    return {
        "success": "脚本结束",
    }


# 查询并获取指令
@router.get("/getscript")
async def get_script():
    script_list = script_service.get_script(BaseConfig.CONFIG_FILE)
    return script_list



