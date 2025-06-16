# db操作

import sqlite3
import geoMaster.schema
import geoMaster.BaseConfig as BaseConfig

# 创建新的连接与游标
def get_cursor(dbname):
    db_path=BaseConfig.ROOT_DIR+'/db/'+dbname+'.db'
    cnx = sqlite3.connect(db_path)
    cur = cnx.cursor()
    return cnx,cur

# 释放连接与游标
def delete_cursor(cnx,cur):
    cur.close()
    cnx.commit()
    cnx.close()

# 做select操作
def select_ope(cur,select_sql):
    cur.execute(select_sql)
    res=cur.fetchall()
    return res

# 做insert操作
def insert_ope(cur,insert_sql,data):
    cur.execute(insert_sql,data)
