import datetime

from fastapi import APIRouter, BackgroundTasks
from geoMaster.SkyLogger import get_logger
from geoMaster.service import child_service
from geoMaster.schema.all_schema import ChildInfo, PureInfo
from geoMaster.utils import global_params
from geoMaster.BaseConfig.base_config import BaseConfig

router = APIRouter(
    prefix="/child",
    tags=["child"],
    responses={404: {"description": "Not found"}}
)

logger = get_logger("child")


# 测试组件
@router.post("/")
async def test_users():
    return {"child_api_status": "ok"}

# 查询组件在线
@router.post("/heartbeat")
async def heart_beat():
    timestamp = datetime.datetime.now()
    child_list=child_service.get_connected_child_info()
    return {
        "success": True,
        "timestamp": timestamp,
        "childlist":child_list
    }

# 查询组件详细信息
@router.post("/nodeinfo")
async def heart_beat():
    pass

@router.post("/recvinfo")
async def recv_info(someinfo: PureInfo):
    # 将获得的数据存储到接收缓冲区内即可
    # 传输的数据应该具有uuid标识
    data_packet = someinfo.info
    uuid = data_packet['uuid']
    data = data_packet['data']
    logger.info(f"[test]message from son:{data}")
    if data.get("info", None) == BaseConfig.INS_ERROR:  # 高优先级消息（错误中断）
        logger.info(f"[test]varname from error:{child_service.get_var_name(uuid)}")  
        global_params.set_valid_from_global(child_service.get_var_name(uuid), False)
        # child_service.master_set_data2recv(uuid, data)
    else:
        child_service.master_set_data2recv(uuid, data)
    return {"child_recvinfo_status": "ok"}


# 注册子节点
@router.post("/register")
async def child_register(ci: ChildInfo):
    try:
        logger.info(ci)
        child_service.child_register(ci)
        return {"child_register_status": "ok"}
    except:
        return {"child_register_status": "fail"}


# 触发主节点向子节点发送信息
@router.post("/sendinfo")
async def child_send_info(info: PureInfo, bt: BackgroundTasks):
    try:
        child_service.send_info_child(info.dict(), bt)
        return {"child_sendinfo_status": "ok"}
    except:
        return {"child_sendinfo_status": "fail"}


# 父节点接收子节点消息
@router.post("/getinfo")
async def get_child_info(info: PureInfo):
    try:
        data = info.info.get("info")
        return {"child_sendinfo_status": "ok"}, data
    except:
        return {"child_sendinfo_status": "fail"}


# 展示子节点
@router.post("/show")
async def show_child_info():
    try:
        print(child_service.child_dict)
        return {"child_register_status": "ok"}
    except:
        return {"child_register_status": "fail"}
