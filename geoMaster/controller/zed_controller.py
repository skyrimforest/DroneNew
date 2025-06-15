from fastapi import APIRouter
import geoMaster.BaseConfig as BaseConfig
from geoMaster.SkyLogger import get_logger
from geoMaster.service import zed_service


router = APIRouter(
    prefix="/zed",
    tags=["zed"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("zed")


# 测试组件在线
@router.post("/")
async def test_users():
    return [{"child_api_status": "ok"}]

# 给出频谱图
@router.get("/frequency")
async def get_frequency():
    x, y = zed_service.get_frequency_data_master_memory()
    return [{
        "name": "master",
        "data": {"x": x, "y": y}
    }]

# 给出频谱图
@router.get("/frequency/child")
async def get_frequency():
    x_y_dicts = zed_service.get_frequency_data_child()
    return x_y_dicts

@router.get("/marker")
async def get_marker():
    target_list = zed_service.get_marker_list()
    print(target_list)
    return {
        "success":True,
        "data": target_list
    }

