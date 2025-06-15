'''
@Project ：pyfw01 
@File    ：user_holder.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/10/16 20:01 
'''
import contextvars
import datetime
from schema.all_schema import UserInfo
user_holder = contextvars.ContextVar(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))

default_user_info = UserInfo(id="0",nick_name="skyrim",icon="null")
default_user_token=user_holder.set(default_user_info)

def save_user(user_info:UserInfo):
    global user_holder
    user_holder.set(user_info)

def get_user():
    global user_holder
    return user_holder.get()

def del_user():
    global user_holder,default_user_token
    user_holder.reset(default_user_token)


if __name__ == '__main__':
    print(user_holder.get())