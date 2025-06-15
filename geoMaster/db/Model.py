import sqlite3

conn=sqlite3.connect("database.db")
cur=conn.cursor()

# 表中对应的类都在schema文件夹下
# 表1: userinfo

# ------------创建阶段------------

# class ChildInfo(BaseModel):
#     uuid:str              # 本次事务uid
#     child_name: str       # 子节点名称
#     child_ip: str         # 子节点ip
#     child_port: str       # 子节点port
# 另外会自动添加id作为主键,同时记录注册时间
child_info_table_sql="""
create table if not exists imageinfo (
    id INTEGER PRIMARY KEY,
    uuid TEXT,
    child_name TEXT,
    child_ip_port TEXT,
    start_time TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
)
"""

# ------------执行阶段------------
cur.execute(
    child_info_table_sql
)

conn.commit()
conn.close()

