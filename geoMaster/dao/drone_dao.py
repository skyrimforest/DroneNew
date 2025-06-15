'''
@Project ：pyfw01 
@File    ：drone_dao.py
@IDE     ：PyCharm 
@Author  ：Skyrim
@Date    ：2024/10/6 9:01 
'''
from geoMaster.utils import db_ope
import os

# drone数据库:
# id,型号,频段,位置,更新时间

def get_drone_data_from_file(file_name):
    f = open(file_name, 'r')
    data=f.readline()
    f.close()
    return data

def insert_drone_data(data):
    cnx, cur = db_ope.get_cursor("database")
    insert_sql = """
    insert into droneinfo (
    drone_type,
    frequency,
    place,
    detect_time
    ) 
   VALUES 
   (?,?,?,?)
    """
    db_ope.insert_ope(cur,insert_sql,data)
    db_ope.delete_cursor(cnx,cur)


def get_drone_data_len():
    cnx, cur = db_ope.get_cursor("database")
    select_sql = """
    select count(*) from droneinfo
     """
    res=db_ope.select_ope(cur,select_sql)
    db_ope.delete_cursor(cnx, cur)
    return res

if __name__ == '__main__':
    pass