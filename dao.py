import pymssql
import pandas as pd

host = '127.0.0.1'  # 'dd.whusoft.cn'
port = '1433'
user = 'sa'
password = 'zww123456'  # '15212xXX'
database = 'self_order'

connection = pymssql.connect(host=host, port=port, user=user, password=password, database=database, charset='utf8')


# 从数据库获取dataframe
def get_df_from_db(sql):
    return pd.read_sql(sql, connection)


def get_city_id():
    sql = 'select * from [city]'
    return get_df_from_db(sql)


