# 引入http网口规范
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# 引入服务器
import uvicorn
# 引入命令行参数读取
import argparse
# 引入路由控件
from controller import child_controller,ai_controller,zed_controller,decoder_controller
# 引入基本配置
import BaseConfig

# 引入zed通信服务组件
from service import work_service

app = FastAPI()
app.include_router(child_controller.router)
app.include_router(zed_controller.router)
app.include_router(ai_controller.router)
app.include_router(decoder_controller.router)

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
        "--host", type=str, default=BaseConfig.HOST_IP, help="Host to bind"
    )
    parser.add_argument(
        "--port", type=int, default=BaseConfig.HOST_PORT, help="Port to bind"
    )
    parser.add_argument(
        "--venv", type=str, default="pureFast", help="Virtual environment to use"
    )
    return parser.parse_args()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 功能状态机:
#   系统启动
#   ->注册阶段,注册一个之后即可开始进行服务,之后也可不断注册子节点
#   ->服务阶段,完成正常的服务需求
#   ->停止阶段,系统正常关闭,持久化记录本次事务

# 这里的线程不需要join,因为系统持续运行不需要阻塞
# client_thread.join()
# 启动所有线程运行
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    # zed_service.run_tcp_client_and_save_data()
    # zed_service.run_fft()
    work_service.run_work_thread()
    yield  # 应用运行中
    # 关闭时执行

if __name__ == '__main__':
    uvicorn.run("main:app", host=BaseConfig.HOST_IP, port=BaseConfig.HOST_PORT)
