import pymysql
import pandas as pd

# 创建数据库连接
conn = pymysql.connect(
    host = '127.0.0.1', # 连接主机, 默认127.0.0.1
    user = 'root',      # 用户名
    passwd = '198557157',# 密码
    port = 3306,        # 端口，默认为3306
    db = 'mydetect',        # 数据库名称
    charset = 'utf8'    # 字符编码
)


# 读取本地excel文件
data = pd.read_excel(r"C:\Users\29392\Desktop\yolov5-master\vermin_names.xlsx")

list1 = data['中文名'].to_list()
list2 = data['图片路径'].to_list()
list3 = data['详细介绍'].to_list()

cursor = conn.cursor()
sql_del = "delete from vermin_trans"
cursor.execute(sql_del)
cursor.connection.commit()

for i in range(len(list1)):
    sql_login = "insert into vermin_trans values(%d,'%s','%s','%s');" % (i, list1[i], list2[i], list3[i])
    cursor.execute(sql_login)
    cursor.connection.commit()

sql_test = "select * from vermin_trans;"
cursor.execute(sql_test)
res = cursor.fetchall()
print(res)
