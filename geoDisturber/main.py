# 引入http网口规范
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 引入服务器
import uvicorn
# 引入命令行参数读取
import argparse

from geoDisturber.BaseConfig.base_config import BaseConfig
# 引入路由控件
from geoDisturber.controller import script_controller, trap_controller

# ========= 日志配置 =========
import logging


class IgnoreOptionsFilter(logging.Filter):
    """过滤掉 uvicorn.access 的 OPTIONS 日志"""

    def filter(self, record: logging.LogRecord) -> bool:
        return "OPTIONS" not in record.getMessage()


# 获取 uvicorn.access 的 logger
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addFilter(IgnoreOptionsFilter())

app = FastAPI()
app.include_router(script_controller.router)
app.include_router(trap_controller.router)

# 处理cors问题
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 接收环境变量
def parse_args():
    parser = argparse.ArgumentParser(description="Run FastAPI server")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind"
    )
    parser.add_argument(
        "--port", type=int, default=10002, help="Port to bind"
    )
    parser.add_argument(
        "--venv", type=str, default="pureFast", help="Virtual environment to use"
    )
    return parser.parse_args()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run("geoDisturber.main:app", host=BaseConfig.HOST_IP, port=BaseConfig.HOST_PORT, reload=False,
                access_log=True)
