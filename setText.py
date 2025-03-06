import os
# 先创建.txt文件所在的文件夹
txt_path = './vermin_describle'
if not os.path.exists(txt_path):
    os.makedirs(txt_path)

# 创建test.txt文件
for i in range(1,95):
    fp = open("./vermin_describle/%s.txt"%(i), "w")