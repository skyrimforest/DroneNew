'''
@Project ：pyfw01 
@File    ：refresh_interceptor.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/10/18 15:41 
'''
# 刷新token的拦截器
import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
class RefreshInterceptor(object):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()  # 记录开始时间
        response = await call_next(request)  # 处理请求
        process_time = round(time.time() - start_time, 4)  # 计算处理时间
        response.headers['X-Process-Time'] = f"{process_time} (s)"  # 添加处理时间到响应头
        return response