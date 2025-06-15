'''
@Project ：pyfw01 
@File    ：model.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/10/6 9:12 
'''
from geoMaster.utils import db_ope

cnx,cur=db_ope.get_cursor("database")


# ------------创建阶段------------
# class DroneInfo(BaseModel):
#     ID
#     drone_type:str            # 型号
#     frequency:str             # 频段
#     place:str                 # 位置
#     detect_time:str           # 检测到的时间
#     appear_time
drone_info_table_sql="""
create table if not exists droneinfo (
    id INTEGER PRIMARY KEY,
    drone_type TEXT,
    frequency TEXT,
    place TEXT,
    detect_time TEXT,
    appear_time TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','localtime'))
)
"""

cur.execute(
    drone_info_table_sql
)

db_ope.delete_cursor(cnx,cur)


