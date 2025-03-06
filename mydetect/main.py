from login_first import login
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from detect_main import Detect
import cv2
import pymysql
import threading
from detect import Thread_1
from detect import trans
import datetime
import os
from manager import Manager
from return_info import return_info

# 创建数据库连接
conn = pymysql.connect(
    host = '127.0.0.1', # 连接主机, 默认127.0.0.1
    user = 'root',      # 用户名
    passwd = '198557157',# 密码
    port = 3306,        # 端口，默认为3306
    db = 'mydetect',        # 数据库名称
    charset = 'utf8'    # 字符编码
)

class stay():
    isTrue = 0
    combox_cur = 0
    iou = 0
    conf = 0

class personal_infor():
    userid = 0
    username = 0


flag = 0
stay_test = stay()
psinfor = personal_infor()

class back(QMainWindow, return_info):
    def __init__(self):
        super().__init__()


        self.setupUi(self)



    def send(self):
        cursor = conn.cursor()
        sql_login = "insert into back_infor values(1,'%s','%s','%s','');"%(self.lineEdit.text(),self.lineEdit_2.text(),self.textEdit.toPlainText())
        cursor.execute(sql_login)
        conn.commit()

        QMessageBox.about(self, "系统提示信息", "发送成功！！！")
        self.close()

class manager(QMainWindow, Manager):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.cnt = 0

        self.cur_back_cnt = 1
        self.back_cnt = 0
        self.all_people = 0


        self.setupUi(self)

    def send_ret(self):
        cursor = conn.cursor()
        sql = "update back_infor set retinfo='%s' where userid='%s';"%(self.TextEdit_1.toPlainText(),self.lineEdit3.text())
        cursor.execute(sql)
        conn.commit()

        QMessageBox.about(self, "系统提示信息", "回馈成功！！！")

    def save(self):
        cursor = conn.cursor()
        sql = 'delete from login;'
        cursor.execute(sql)
        conn.commit()

        for i in range(self.all_people):
            txt1 = self.model.data(self.model.index(i,0))
            txt2 = self.model.data(self.model.index(i,1))
            sql = "insert into login values('%s','%s')"%(txt1,txt2)
            cursor.execute(sql)
            conn.commit()
        QMessageBox.about(self, "系统提示信息", "保存成功！！！")


    def delete(self):
        cursor = conn.cursor()
        index = self.tableView.currentIndex()  # 取得当前选中行的index
        text1 = self.model.data(self.model.index(index.row(), 0))
        text2 = self.model.data(self.model.index(index.row(), 1))
        sql = "delete from login where id='%s' and name='%s';" % (text1, text2)
        cursor.execute(sql)
        conn.commit()

        self.model.removeRow(index.row())  # 通过index的row()操作得到行数进行删除

    def trans_left(self):
        cursor = conn.cursor()
        sql = "select * from back_infor;"
        cursor.execute(sql)
        res = cursor.fetchall()

        if len(res) == 1:
            QMessageBox.about(self, "系统提示信息", "无其他反馈！！！")
        else:
            self.cur_back_cnt-=1
            if self.cur_back_cnt==0:
                self.cur_back_cnt=self.back_cnt

            self.lineEdit3.setText('%s' % (res[self.cur_back_cnt-1][1]))
            self.lineEdit4.setText('%s' % (res[self.cur_back_cnt-1][2]))
            self.TextEdit.setText('%s' % (res[self.cur_back_cnt-1][3]))


    def trans_right(self):
        cursor = conn.cursor()
        sql = "select * from back_infor;"
        cursor.execute(sql)
        res = cursor.fetchall()

        if len(res) == 1:
            QMessageBox.about(self, "系统提示信息", "无其他反馈！！！")
        else:
            self.cur_back_cnt += 1
            if self.cur_back_cnt == self.back_cnt+1:
                self.cur_back_cnt = 1

            self.lineEdit3.setText('%s' % (res[self.cur_back_cnt - 1][1]))
            self.lineEdit4.setText('%s' % (res[self.cur_back_cnt - 1][2]))
            self.TextEdit.setText('%s' % (res[self.cur_back_cnt - 1][3]))

    def exit_login(self):
        self.hide()
        self.main_frame = main()
        self.main_frame.show()


    def save_trans(self):
        global stay_test
        stay_test.combox_cur = self.combox.currentText()
        stay_test.iou = int(self.lineEdit1.text())
        stay_test.conf = int(self.lineEdit2.text())
        stay_test.isTrue = 1

        QMessageBox.about(self, "系统提示信息", "保存成功！！！")

    def show_sArea(self):
        height = 20

        cursor = conn.cursor()
        sql_login = "select * from Talk;"
        cursor.execute(sql_login)
        res = cursor.fetchall()
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 937, 10000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(937, 10000))

        for i in range(len(res)):
            label_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label_text.setText("%s"%res[i][0])
            label_text.setGeometry(QtCore.QRect(10,20+height,700,100))
            label_text.setStyleSheet("background-color:white;border-radius: 10px;border-color:rgb(255,170,0);")

            btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            btn.setText('删除')
            btn.setGeometry(QtCore.QRect(720,35+height,50,40))

            label_date = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label_date.setText("%s"%res[i][1])
            label_date.setGeometry(QtCore.QRect(10, 120+height, 700, 30))
            label_date.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            height+=150

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def hide1(self):
        cursor = conn.cursor()
        sql_login = "select * from login;"
        cnt = cursor.execute(sql_login)
        res = cursor.fetchall()
        self.all_people = cnt

        self.model.removeRows(0, self.model.rowCount())
        for i in range(0,cnt):
            for j in range(0,2):
                item = QStandardItem('%s'%(res[i][j]))
                self.model.setItem(i,j,item)
        self.tableView.setModel(self.model)

        #1
        self.tableView.setVisible(True)
        self.btn1.setVisible(True)
        self.btn2.setVisible(True)

        #2
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.lineEdit2.setVisible(False)
        self.lineEdit1.setVisible(False)
        self.combox.setVisible(False)
        self.pushButton_4.setVisible(False)

        # 3
        self.pushButton_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.TextEdit.setVisible(False)
        self.label_11.setVisible(False)
        self.TextEdit_1.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(False)

        # 4
        self.tableView1.setVisible(False)
        self.pushButton_20.setVisible(False)
        self.pushButton_21.setVisible(False)

        # 5
        self.label_30.setVisible(False)
        self.label_31.setVisible(False)
        self.label_32.setVisible(False)
        self.pushButton_30.setVisible(False)
        self.pushButton_31.setVisible(False)
        self.pushButton_32.setVisible(False)
        self.pushButton_33.setVisible(False)
        self.pushButton_34.setVisible(False)
        self.pushButton_35.setVisible(False)

        # 6
        self.label_40.setVisible(False)
        self.label_41.setVisible(False)
        self.label_42.setVisible(False)
        self.pushButton_40.setVisible(False)
        self.pushButton_41.setVisible(False)
        self.pushButton_42.setVisible(False)
        self.pushButton_43.setVisible(False)
        self.pushButton_44.setVisible(False)
        self.pushButton_45.setVisible(False)

        # 7
        self.scrollArea.setVisible(False)

    def hide2(self):
        # 初始化
        if self.cnt==0:
            files = os.listdir('../weights/')
            for i in range(len(files)):
                self.combox.addItem(files[i])
        self.cnt+=1

        self.label_4.setVisible(True)
        self.label_5.setVisible(True)
        self.label_6.setVisible(True)
        self.label_7.setVisible(True)
        self.lineEdit2.setVisible(True)
        self.lineEdit1.setVisible(True)
        self.combox.setVisible(True)
        self.pushButton_4.setVisible(True)

        # 1
        self.tableView.setVisible(False)
        self.btn1.setVisible(False)
        self.btn2.setVisible(False)

        #3
        self.pushButton_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.TextEdit.setVisible(False)
        self.label_11.setVisible(False)
        self.TextEdit_1.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(False)

        # 4
        self.tableView1.setVisible(False)
        self.pushButton_20.setVisible(False)
        self.pushButton_21.setVisible(False)

        # 5
        self.label_30.setVisible(False)
        self.label_31.setVisible(False)
        self.label_32.setVisible(False)
        self.pushButton_30.setVisible(False)
        self.pushButton_31.setVisible(False)
        self.pushButton_32.setVisible(False)
        self.pushButton_33.setVisible(False)
        self.pushButton_34.setVisible(False)
        self.pushButton_35.setVisible(False)
        # 6
        self.label_40.setVisible(False)
        self.label_41.setVisible(False)
        self.label_42.setVisible(False)
        self.pushButton_40.setVisible(False)
        self.pushButton_41.setVisible(False)
        self.pushButton_42.setVisible(False)
        self.pushButton_43.setVisible(False)
        self.pushButton_44.setVisible(False)
        self.pushButton_45.setVisible(False)

        # 7
        self.scrollArea.setVisible(False)

    def hide3(self):
        cursor = conn.cursor()
        sql = "select * from back_infor;"
        cursor.execute(sql)
        res = cursor.fetchall()
        self.back_cnt = len(res)

        self.lineEdit3.setText('%s'%(res[0][1]))
        self.lineEdit4.setText('%s'%(res[0][2]))
        self.TextEdit.setText('%s'%(res[0][3]))
        self.TextEdit_1.setText('%s'%(res[0][4]))

        self.pushButton_7.setVisible(True)
        self.label_8.setVisible(True)
        self.label_9.setVisible(True)
        self.label_10.setVisible(True)
        self.lineEdit3.setVisible(True)
        self.lineEdit4.setVisible(True)
        self.TextEdit.setVisible(True)
        self.label_11.setVisible(True)
        self.TextEdit_1.setVisible(True)
        self.pushButton_5.setVisible(True)
        self.pushButton_6.setVisible(True)

        # 1
        self.tableView.setVisible(False)
        self.btn1.setVisible(False)
        self.btn2.setVisible(False)

        #2
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.lineEdit2.setVisible(False)
        self.lineEdit1.setVisible(False)
        self.combox.setVisible(False)
        self.pushButton_4.setVisible(False)

        # 4
        self.tableView1.setVisible(False)
        self.pushButton_20.setVisible(False)
        self.pushButton_21.setVisible(False)

        # 5
        self.label_30.setVisible(False)
        self.label_31.setVisible(False)
        self.label_32.setVisible(False)
        self.pushButton_30.setVisible(False)
        self.pushButton_31.setVisible(False)
        self.pushButton_32.setVisible(False)
        self.pushButton_33.setVisible(False)
        self.pushButton_34.setVisible(False)
        self.pushButton_35.setVisible(False)
        # 6
        self.label_40.setVisible(False)
        self.label_41.setVisible(False)
        self.label_42.setVisible(False)
        self.pushButton_40.setVisible(False)
        self.pushButton_41.setVisible(False)
        self.pushButton_42.setVisible(False)
        self.pushButton_43.setVisible(False)
        self.pushButton_44.setVisible(False)
        self.pushButton_45.setVisible(False)

        # 7
        self.scrollArea.setVisible(False)

    def hide4(self):
        cursor = conn.cursor()
        sql = "select name from vermin_trans;"
        cnt = cursor.execute(sql)
        res = cursor.fetchall()

        for i in range(0, cnt):
            item = QStandardItem('%s' % (res[i]))
            self.model1.setItem(i, 0, item)
        self.tableView1.setModel(self.model1)

        self.tableView1.setVisible(True)
        self.pushButton_20.setVisible(True)
        self.pushButton_21.setVisible(True)

        # 1
        self.tableView.setVisible(False)
        self.btn1.setVisible(False)
        self.btn2.setVisible(False)

        # 2
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.lineEdit2.setVisible(False)
        self.lineEdit1.setVisible(False)
        self.combox.setVisible(False)
        self.pushButton_4.setVisible(False)

        # 3
        self.pushButton_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.TextEdit.setVisible(False)
        self.label_11.setVisible(False)
        self.TextEdit_1.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(False)


        # 5
        self.label_30.setVisible(False)
        self.label_31.setVisible(False)
        self.label_32.setVisible(False)
        self.pushButton_30.setVisible(False)
        self.pushButton_31.setVisible(False)
        self.pushButton_32.setVisible(False)
        self.pushButton_33.setVisible(False)
        self.pushButton_34.setVisible(False)
        self.pushButton_35.setVisible(False)
        # 6
        self.label_40.setVisible(False)
        self.label_41.setVisible(False)
        self.label_42.setVisible(False)
        self.pushButton_40.setVisible(False)
        self.pushButton_41.setVisible(False)
        self.pushButton_42.setVisible(False)
        self.pushButton_43.setVisible(False)
        self.pushButton_44.setVisible(False)
        self.pushButton_45.setVisible(False)

        # 7
        self.scrollArea.setVisible(False)



    def hide5(self):
        self.label_30.setVisible(True)
        self.label_31.setVisible(True)
        self.label_32.setVisible(True)
        self.pushButton_30.setVisible(True)
        self.pushButton_31.setVisible(True)
        self.pushButton_32.setVisible(True)
        self.pushButton_33.setVisible(True)
        self.pushButton_34.setVisible(True)
        self.pushButton_35.setVisible(True)

        # 1
        self.tableView.setVisible(False)
        self.btn1.setVisible(False)
        self.btn2.setVisible(False)

        # 2
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.lineEdit2.setVisible(False)
        self.lineEdit1.setVisible(False)
        self.combox.setVisible(False)
        self.pushButton_4.setVisible(False)

        # 3
        self.pushButton_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.TextEdit.setVisible(False)
        self.label_11.setVisible(False)
        self.TextEdit_1.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(False)

        # 4
        self.tableView1.setVisible(False)
        self.pushButton_20.setVisible(False)
        self.pushButton_21.setVisible(False)

        # 6
        self.label_40.setVisible(False)
        self.label_41.setVisible(False)
        self.label_42.setVisible(False)
        self.pushButton_40.setVisible(False)
        self.pushButton_41.setVisible(False)
        self.pushButton_42.setVisible(False)
        self.pushButton_43.setVisible(False)
        self.pushButton_44.setVisible(False)
        self.pushButton_45.setVisible(False)

        # 7
        self.scrollArea.setVisible(False)

    def hide6(self):
        self.label_40.setVisible(True)
        self.label_41.setVisible(True)
        self.label_42.setVisible(True)
        self.pushButton_40.setVisible(True)
        self.pushButton_41.setVisible(True)
        self.pushButton_42.setVisible(True)
        self.pushButton_43.setVisible(True)
        self.pushButton_44.setVisible(True)
        self.pushButton_45.setVisible(True)
        # 1
        self.tableView.setVisible(False)
        self.btn1.setVisible(False)
        self.btn2.setVisible(False)

        # 2
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.lineEdit2.setVisible(False)
        self.lineEdit1.setVisible(False)
        self.combox.setVisible(False)
        self.pushButton_4.setVisible(False)

        # 3
        self.pushButton_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.TextEdit.setVisible(False)
        self.label_11.setVisible(False)
        self.TextEdit_1.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(False)

        # 4
        self.tableView1.setVisible(False)
        self.pushButton_20.setVisible(False)
        self.pushButton_21.setVisible(False)

        # 5
        self.label_30.setVisible(False)
        self.label_31.setVisible(False)
        self.label_32.setVisible(False)
        self.pushButton_30.setVisible(False)
        self.pushButton_31.setVisible(False)
        self.pushButton_32.setVisible(False)
        self.pushButton_33.setVisible(False)
        self.pushButton_34.setVisible(False)
        self.pushButton_35.setVisible(False)

        # 7
        self.scrollArea.setVisible(False)

    def hide7(self):
        self.scrollArea.setVisible(True)
        self.show_sArea()

        # 1
        self.tableView.setVisible(False)
        self.btn1.setVisible(False)
        self.btn2.setVisible(False)

        # 2
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.lineEdit2.setVisible(False)
        self.lineEdit1.setVisible(False)
        self.combox.setVisible(False)
        self.pushButton_4.setVisible(False)

        # 3
        self.pushButton_7.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.label_10.setVisible(False)
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.TextEdit.setVisible(False)
        self.label_11.setVisible(False)
        self.TextEdit_1.setVisible(False)
        self.pushButton_5.setVisible(False)
        self.pushButton_6.setVisible(False)

        # 4
        self.tableView1.setVisible(False)
        self.pushButton_20.setVisible(False)
        self.pushButton_21.setVisible(False)

        # 5
        self.label_30.setVisible(False)
        self.label_31.setVisible(False)
        self.label_32.setVisible(False)
        self.pushButton_30.setVisible(False)
        self.pushButton_31.setVisible(False)
        self.pushButton_32.setVisible(False)
        self.pushButton_33.setVisible(False)
        self.pushButton_34.setVisible(False)
        self.pushButton_35.setVisible(False)

        # 6
        self.label_40.setVisible(False)
        self.label_41.setVisible(False)
        self.label_42.setVisible(False)
        self.pushButton_40.setVisible(False)
        self.pushButton_41.setVisible(False)
        self.pushButton_42.setVisible(False)
        self.pushButton_43.setVisible(False)
        self.pushButton_44.setVisible(False)
        self.pushButton_45.setVisible(False)


class main(QMainWindow,login):
    def __init__(self):
        super().__init__()

        self.setupUi(self)




    def login_main(self):
        data1 = self.lineEdit.text()
        data2 = self.lineEdit_2.text()

        if self.radiobtn1.isChecked() == True:
            cursor = conn.cursor()
            sql_login = "select * from login where id='%s' and name='%s';" % (data1, data2)
            cursor.execute(sql_login)
            res = cursor.fetchone()
            if data1 == "" or data2 == "":
                QMessageBox.about(self, "系统提示信息", "账号密码缺失，请重新输入！！！")
                self.del_text()  # 清空输入
            else:
                if res != None:
                    QMessageBox.about(self, "系统提示信息", "密码正确！！！")

                    global psinfor
                    psinfor.userid = data1
                    psinfor.username = data2

                    self.transFrame()
                else:
                    QMessageBox.about(self, "系统提示信息", "密码错误！！！")
            self.del_text()  # 清空输入
        else:
            if data1 == "" or data2 == "":
                QMessageBox.about(self, "系统提示信息", "账号密码缺失，请重新输入！！！")
                self.del_text()  # 清空输入

            else:
                if data1 == "123456" and data2 == "admin":
                    QMessageBox.about(self, "系统提示信息", "密码正确！！！")

                    self.transFrame()
                else:
                    QMessageBox.about(self, "系统提示信息", "密码错误！！！")
            self.del_text()  # 清空输入

    def login_in(self):
        if self.radiobtn1.isChecked() == True:
            cursor = conn.cursor()
            sql_login = "insert into login values('%s','%s');" % (self.lineEdit.text(), self.lineEdit_2.text())
            cursor.execute(sql_login)
            conn.commit()
            QMessageBox.about(self, "系统提示信息", "注册成功！！！")
            self.del_text()  # 清空输入
        else:
            QMessageBox.about(self, "系统提示信息", "管理员仅有一个固定账号！！！")
            self.del_text()  # 清空输入

    def transFrame(self):
        if self.radiobtn1.isChecked() == True:
            self.hide()
            self.frame1 = Detect_frame()
            self.frame1.show()
            self.frame1.hide1()
        else:
            self.hide()
            self.frame2 = manager()
            self.frame2.show()
            self.frame2.hide1()

    def del_text(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")



class Detect_frame(QMainWindow,Detect):
    def __init__(self):
        super().__init__()
        self.cnt = 0
        self.timer_camera = QTimer()

        self.thread = Thread_1()
        self.timer_camera.timeout.connect(self.show_Vgraph)
        self.cur_vermin = 0

        self.model = 0 # 0代表图片，1代表视频，2代表实时摄像头
        self.btn = 0

        self.cur_pic = 0 #推理坐标图片
        self.ensure = 0

        self.setupUi(self)

    def set_progress(self,m):
        self.progressBar.setValue(m)

    def return_back(self):
        global psinfor

        self.test = back()
        self.test.lineEdit.setText('%s'%(psinfor.userid))
        self.test.lineEdit_2.setText('%s'%(psinfor.username))
        self.test.show()

    def exit_login(self):
        self.hide()
        self.main_frame = main()
        self.main_frame.show()

    def spinbox_change_1(self):
        self.hSlider_1.setValue(self.spinbox_1.value())
        trans.iou_thres = round((int(self.spinbox_1.value()) / 100),2)
    def spinbox_change_2(self):
        self.hSlider_2.setValue(self.spinbox_2.value())
        trans.conf_thres = round((int(self.spinbox_2.value()) / 100),2)

    def splider_change_1(self):
        self.spinbox_1.setValue(self.hSlider_1.value())
        trans.iou_thres = round((int(self.hSlider_1.value()) / 100), 2)
    def splider_change_2(self):
        self.spinbox_2.setValue(self.hSlider_2.value())
        trans.conf_thres = round((int(self.hSlider_2.value()) / 100), 2)



    def addTalk(self):
        cursor = conn.cursor()
        sql_login = "insert into Talk values('%s','%s');"%(self.textEdit_5.toPlainText(),datetime.date.today())
        cursor.execute(sql_login)
        conn.commit()

        self.show_sArea()
        self.textEdit_5.setText("")

    def show_sArea(self):
        height = 20

        cursor = conn.cursor()
        sql_login = "select * from Talk;"
        cursor.execute(sql_login)
        res = cursor.fetchall()
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 937, 10000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(937, 10000))

        for i in range(len(res)):
            label_text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label_text.setText("%s"%res[i][0])
            label_text.setGeometry(QtCore.QRect(50,20+height,850,100))
            label_text.setStyleSheet("background-color:white;border-radius: 10px;border-color:rgb(255,170,0);")
            label_date = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label_date.setText("%s"%res[i][1])
            label_date.setGeometry(QtCore.QRect(50, 120+height, 850, 30))
            label_date.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            height+=150

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


    def result_show(self):
        if self.model == 0:
            cnt_str = ""
            label_height = self.label.height()
            label_width = self.label.width()
            img = cv2.imread('temp.jpg')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            height, width, channels = img.shape  ##获取图片宽度
            if height < width:
                img = cv2.resize(img, (label_width, int(label_width * height / width)))
            else:
                img = cv2.resize(img, (int(height * label_width / label_width), label_height))

            a, b, c = img.shape
            byte = 3 * b

            img = QImage(img.data, img.shape[1], img.shape[0], byte,
                         QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.setAlignment(Qt.AlignCenter)
            if trans.isexist == 1:
                for i in range(len(trans.box)):
                    cnt_str += "类别:%s\n置信度：%.2f\n坐标位置:(%s,%s,%s,%s)\n\n"%(trans.box[i][0],trans.box[i][1],
                    trans.box[i][2],trans.box[i][3],trans.box[i][4],trans.box[i][5])
                self.textEdit_2.setText(cnt_str)
                trans.box =[]
                # trans.isexist = 0
            else:
                self.textEdit_2.setText("no detection！！！")
        elif self.model == 1:
            self.label.clear()
            self.cap = cv2.VideoCapture(r'C:\Users\29392\Desktop\yolov5-master\mydetect\temp.mp4')
            self.timer_camera.start(30)
        else:
            self.label.clear()

    def detect_start(self):
        if self.model == 2:
            self.btn = 1
        else:
            self.thread.start()

    def openFilePic(self):
        self.progressBar.setVisible(False)
        self.model = 0
        if self.cnt != 0:
            self.cap.release()
            cv2.destroyAllWindows()
        self.cnt = 0
        self.timer_camera.stop()
        directory1 = QFileDialog.getOpenFileName(self,"选取文件夹","./vermin_pics","All Files(*);")  # 起始路径
        img = cv2.imread(directory1[0])
        label_height = int(self.label.height())
        label_width = int(self.label.width())

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape  ##获取图片宽度

        if height < width:
            img = cv2.resize(img, (label_width, int(label_width * height / width)))
        else:
            img = cv2.resize(img, (int(height * label_width / label_width), label_height))

        a, b, c = img.shape
        byte = 3 * b

        img = QImage(img.data, img.shape[1], img.shape[0], byte,
                     QImage.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(img))
        self.label.setAlignment(Qt.AlignCenter)

        self.thread.source = directory1[0]


    def detect_number(self):
        if self.model==1: #是视频则进度条
            self.timer_camera.start(30)

        start_h = int(self.lineEdit_2.text())
        start_w = int(self.lineEdit_3.text())
        move_h = int(self.lineEdit_8.text())
        move_w = int(self.lineEdit_9.text())
        start_upleft = int(self.lineEdit_4.text())
        start_upright = int(self.lineEdit_5.text())
        start_downleft = int(self.lineEdit_6.text())
        start_downright = int(self.lineEdit_7.text())
        test_1 = int(start_upleft*(move_h/start_h))
        test_2 = int(start_upright*(move_w/start_w))
        test_3 = int(start_downleft*(move_h/start_h))
        test_4 = int(start_downright*(move_w/start_w))
        self.lineEdit_10.setText("%s"%test_1)
        self.lineEdit_11.setText("%s"%test_2)
        self.lineEdit_12.setText("%s"%test_3)
        self.lineEdit_13.setText("%s"%test_4)
        img = cv2.imread('%s'%self.cur_pic)

        img=cv2.resize(img,(move_h,move_w))

        img = cv2.rectangle(img, (test_1, test_2), (test_3,test_4), (0, 255, 0), 4)
        cv2.imwrite("detect_number.jpg",img)

        label_height = self.label_28.height()
        label_width = self.label_28.width()
        img = cv2.imread('detect_number.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        height, width, channels = img.shape  ##获取图片宽度
        if height < width:
            img = cv2.resize(img, (label_width, int(label_width * height / width)))
        else:
            img = cv2.resize(img, (int(height * label_width / label_width), label_height))

        a, b, c = img.shape
        byte = 3 * b

        img = QImage(img.data, img.shape[1], img.shape[0], byte,
                     QImage.Format_RGB888)

        self.label_28.setPixmap(QPixmap.fromImage(img))
        self.label_28.setAlignment(Qt.AlignCenter)


    def openFileVideo(self):
        self.progressBar.setVisible(True)
        self.textEdit_2.setText("视频检测不显示坐标信息")
        trans.progress_cnt=0
        self.model = 1
        if self.cnt != 0:
            self.cap.release()
            cv2.destroyAllWindows()
        self.cnt = 1
        self.timer_camera.stop()
        video_path = QFileDialog.getOpenFileName(self,"选取文件夹","./vermin_videos","All Files(*);")  # 起始路径
        self.cap = cv2.VideoCapture(video_path[0])
        self.timer_camera.start(30)

        self.thread.source = video_path[0]

    def openVgraph(self):
        self.model = 2
        self.progressBar.setVisible(False)
        self.thread.source = r'C:\Users\29392\Desktop\yolov5-master\mydetect\temp_time.jpg'
        if self.cnt != 0:
            self.cap.release()
            cv2.destroyAllWindows()
        self.cnt = 1
        self.cap = cv2.VideoCapture(0)
        self.timer_camera.start(2000)



    def show_Vgraph(self):
        if self.model==1:#是视频的清空下调用进度条
            self.progressBar.setValue(int(trans.progress_cnt/712*100))

        ret, frame = self.cap.read()
        global cnt
        if ret is True:
            if self.model == 2 and self.btn == 1:

                cv2.imwrite('temp_time.jpg',frame)
                self.thread.start()
                if cnt ==0 :
                    self.label.clear()
                    cnt+=1
                else:
                    img = cv2.imread(r'C:\Users\29392\Desktop\yolov5-master\mydetect\temp.jpg')
                    label_height = int(self.label.height())
                    label_width = int(self.label.width())

                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    height, width, channels = img.shape  ##获取图片宽度

                    if height < width:
                        if label_height > height:
                            img = cv2.resize(img, (int(height * label_width / label_width), label_height))
                        else:
                            img = cv2.resize(img, (label_width, int(label_width * height / width)))
                    else:
                        if label_width > width:
                            img = cv2.resize(img, (int(label_height * width / height), label_height))
                        else:
                            img = cv2.resize(img, (int(height * label_width / label_width), label_height))

                    a, b, c = img.shape
                    byte = 3 * b

                    img = QImage(img.data, img.shape[1], img.shape[0], byte,
                                 QImage.Format_RGB888)

                    self.label.setPixmap(QPixmap.fromImage(img))
                    self.label.setAlignment(Qt.AlignCenter)
            else:
                cnt = 0
                label_height = int(self.label.height())
                label_width = int(self.label.width())

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channels = img.shape  ##获取图片宽度

                if height < width:
                    if label_height > height:
                        img = cv2.resize(img, (int(height * label_width / label_width), label_height))
                    else:
                        img = cv2.resize(img, (label_width, int(label_width * height / width)))
                else:
                    if label_width > width:
                        img = cv2.resize(img, (int(label_height*width/height),label_height))
                    else:
                        img = cv2.resize(img, (int(height * label_width / label_width), label_height))

                a, b, c = img.shape
                byte = 3 * b

                img = QImage(img.data, img.shape[1], img.shape[0], byte,
                             QImage.Format_RGB888)

                self.label.setPixmap(QPixmap.fromImage(img))
                self.label.setAlignment(Qt.AlignCenter)
        # else:
        #     self.label.clear()



    def select_vermin(self):
        cursor = conn.cursor()

        sql_login = "select * from vermin_trans where name='%s';"%(self.lineEdit.text())
        cursor.execute(sql_login)
        res = cursor.fetchone()
        img = cv2.imread(res[2],-1)

        label_height = self.label_16.height()
        label_width = self.label_16.width()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape  ##获取图片宽度
        if height < width:
            if label_height > height:
                img = cv2.resize(img, (int(height * label_width / label_width), label_height))
            else:
                img = cv2.resize(img, (label_width, int(label_width * height / width)))
        else:
            if label_width > width:
                img = cv2.resize(img, (int(label_height * width / height), label_height))
            else:
                img = cv2.resize(img, (int(height * label_width / label_width), label_height))
        a, b, c = img.shape
        byte = 3 * b
        img = QImage(img.data, img.shape[1], img.shape[0], byte,
                     QImage.Format_RGB888)
        self.label_16.setPixmap(QPixmap.fromImage(img))
        self.label_16.setAlignment(Qt.AlignCenter)
        self.lineEdit_1.setText(res[1])
        self.textEdit.setText(res[3])

    def tran_left(self):
        self.cur_vermin-=1
        if self.cur_vermin==-1:
            self.cur_vermin=93
        cursor = conn.cursor()
        sql_login = "select * from vermin_trans where id='%s';" % (self.cur_vermin)
        cursor.execute(sql_login)
        res = cursor.fetchone()
        label_height = int(self.label_16.height())
        label_width = int(self.label_16.width())

        img = cv2.imread(res[2])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape  ##获取图片宽度
        if height < width:
            img = cv2.resize(img, (label_width, int(label_width * height / width)))
        else:
            img = cv2.resize(img, (int(height * label_width / label_width), label_height))

        a, b, c = img.shape
        byte = 3 * b

        img = QImage(img.data, img.shape[1], img.shape[0], byte,
                     QImage.Format_RGB888)
        self.label_16.setPixmap(QPixmap.fromImage(img))
        self.label_16.setAlignment(Qt.AlignCenter)
        self.lineEdit_1.setText(res[1])
        self.textEdit.setText(res[3])

    def tran_right(self):
        self.cur_vermin+=1
        if self.cur_vermin==94:
            self.cur_vermin=0
        cursor = conn.cursor()
        sql_login = "select * from vermin_trans where id='%s';" % (self.cur_vermin)
        cursor.execute(sql_login)
        res = cursor.fetchone()
        label_height = int(self.label_16.height())
        label_width = int(self.label_16.width())

        img = cv2.imread(res[2])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape  ##获取图片宽度
        if height < width:
            img = cv2.resize(img, (label_width, int(label_width * height / width)))
        else:
            img = cv2.resize(img, (int(height * label_width / label_width), label_height))

        a, b, c = img.shape
        byte = 3 * b

        img = QImage(img.data, img.shape[1], img.shape[0], byte,
                     QImage.Format_RGB888)
        self.label_16.setPixmap(QPixmap.fromImage(img))
        self.label_16.setAlignment(Qt.AlignCenter)
        self.lineEdit_1.setText(res[1])
        self.textEdit.setText(res[3])

    def changePT(self):
        trans.weights="weights/%s"%(self.combox.currentText())


    def hide1(self):
        #vermin一览
        # 1
        self.pushButton.setVisible(True)
        self.lineEdit.setVisible(True)
        self.label_16.setVisible(True)
        self.label_17.setVisible(True)
        self.label_18.setVisible(True)
        self.lineEdit_1.setVisible(True)
        self.textEdit.setVisible(True)
        self.pushButton_12.setVisible(True)
        self.pushButton_13.setVisible(True)


        cursor = conn.cursor()
        sql_test = "select * from vermin_trans;"
        cursor.execute(sql_test)
        res = cursor.fetchone()

        label_height = int(self.label_16.height())
        label_width = int(self.label_16.width())

        img = cv2.imread(res[2])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape  ##获取图片宽度
        if height < width:
            img = cv2.resize(img,(label_width,int(label_width*height/width)))
        else:
            img = cv2.resize(img,(int(height*label_width/label_width),label_height))

        a,b,c = img.shape
        byte = 3 * b

        img = QImage(img.data,img.shape[1],img.shape[0],byte,
                        QImage.Format_RGB888)
        self.label_16.setPixmap(QPixmap.fromImage(img))
        self.label_16.setAlignment(Qt.AlignCenter)

        self.lineEdit_1.setText(res[1])
        self.textEdit.setText(res[3])

        # 2
        self.label.setVisible(False)
        self.textEdit_2.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.label_11.setVisible(False)
        self.label_13.setVisible(False)
        self.label_14.setVisible(False)
        self.label_15.setVisible(False)
        self.progressBar.setVisible(False)
        self.pushButton_6.setVisible(False)
        self.pushButton_7.setVisible(False)
        self.pushButton_8.setVisible(False)
        self.pushButton_9.setVisible(False)
        self.pushButton_11.setVisible(False)
        self.combox.setVisible(False)
        self.spinbox_1.setVisible(False)
        self.spinbox_2.setVisible(False)
        self.hSlider_1.setVisible(False)
        self.hSlider_2.setVisible(False)

        # 3
        self.tableView.setVisible(False)
        self.lb1.setVisible(False)
        self.lb2.setVisible(False)
        self.lb3.setVisible(False)
        self.lb4.setVisible(False)
        self.lb5.setVisible(False)
        self.lb6.setVisible(False)
        self.mail.setVisible(False)
        self.LEdit.setVisible(False)
        self.rdio.setVisible(False)
        self.rdio1.setVisible(False)
        self.dEdit.setVisible(False)
        self.pBtn.setVisible(False)


        # 4
        self.pushButton_15.setVisible(False)
        self.textEdit_5.setVisible(False)
        self.scrollArea.setVisible(False)
        self.scrollAreaWidgetContents.setVisible(False)

    def hide2(self):
        #初始化
        if self.ensure == 0:
            files = os.listdir('../weights/')
            for i in range(len(files)):
                self.combox.addItem(files[i])
            self.ensure+=1

        global stay_test

        if stay_test.isTrue == 1:
            self.combox.setCurrentText(stay_test.combox_cur)
            self.hSlider_1.setValue(stay_test.iou)
            self.hSlider_2.setValue(stay_test.conf)
            stay_test.isTrue = 0

        # detect
        # 2
        self.label.setVisible(True)
        self.label.clear()
        self.textEdit_2.setVisible(True)
        self.label_4.setVisible(True)
        self.label_5.setVisible(True)
        self.label_6.setVisible(True)
        self.label_7.setVisible(True)
        self.label_11.setVisible(False)
        self.label_13.setVisible(True)
        self.label_14.setVisible(True)
        self.label_15.setVisible(True)
        self.progressBar.setVisible(False)
        self.pushButton_6.setVisible(True)
        self.pushButton_7.setVisible(True)
        self.pushButton_8.setVisible(True)
        self.pushButton_9.setVisible(True)
        self.pushButton_11.setVisible(True)
        self.combox.setVisible(True)
        self.spinbox_1.setVisible(True)
        self.spinbox_2.setVisible(True)
        self.hSlider_1.setVisible(True)
        self.hSlider_2.setVisible(True)

        # 1
        self.pushButton.setVisible(False)
        self.lineEdit.setVisible(False)
        self.label_16.setVisible(False)
        self.label_17.setVisible(False)
        self.label_18.setVisible(False)
        self.lineEdit_1.setVisible(False)
        self.textEdit.setVisible(False)
        self.pushButton_12.setVisible(False)
        self.pushButton_13.setVisible(False)

        #3
        self.tableView.setVisible(False)
        self.lb1.setVisible(False)
        self.lb2.setVisible(False)
        self.lb3.setVisible(False)
        self.lb4.setVisible(False)
        self.lb5.setVisible(False)
        self.lb6.setVisible(False)
        self.mail.setVisible(False)
        self.LEdit.setVisible(False)
        self.rdio.setVisible(False)
        self.rdio1.setVisible(False)
        self.dEdit.setVisible(False)
        self.pBtn.setVisible(False)

        # 4
        self.pushButton_15.setVisible(False)
        self.textEdit_5.setVisible(False)
        self.scrollArea.setVisible(False)
        self.scrollAreaWidgetContents.setVisible(False)

    def hide3(self):
        cursor = conn.cursor()
        sql = "select retinfo from back_infor where userid='2020141436';"
        cnt = cursor.execute(sql)
        res = cursor.fetchall()

        for i in range(0,cnt):
            item = QStandardItem('%s'%(res[i][0]))
            self.model.setItem(i,0,item)
        self.tableView.setModel(self.model)


        #3

        self.tableView.setVisible(True)
        self.lb1.setVisible(True)
        self.lb2.setVisible(True)
        self.lb3.setVisible(True)
        self.lb4.setVisible(True)
        self.lb5.setVisible(True)
        self.lb6.setVisible(True)
        self.mail.setVisible(True)
        self.LEdit.setVisible(True)
        self.rdio.setVisible(True)
        self.rdio1.setVisible(True)
        self.dEdit.setVisible(True)
        self.pBtn.setVisible(True)


        #1
        self.pushButton.setVisible(False)
        self.lineEdit.setVisible(False)
        self.label_16.setVisible(False)
        self.label_17.setVisible(False)
        self.label_18.setVisible(False)
        self.lineEdit_1.setVisible(False)
        self.textEdit.setVisible(False)
        self.pushButton_12.setVisible(False)
        self.pushButton_13.setVisible(False)

        #2
        self.label.setVisible(False)
        self.textEdit_2.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.label_11.setVisible(False)
        self.label_13.setVisible(False)
        self.label_14.setVisible(False)
        self.label_15.setVisible(False)
        self.progressBar.setVisible(False)
        self.pushButton_6.setVisible(False)
        self.pushButton_7.setVisible(False)
        self.pushButton_8.setVisible(False)
        self.pushButton_9.setVisible(False)
        self.pushButton_11.setVisible(False)
        self.combox.setVisible(False)
        self.spinbox_1.setVisible(False)
        self.spinbox_2.setVisible(False)
        self.hSlider_1.setVisible(False)
        self.hSlider_2.setVisible(False)

        #4
        self.pushButton_15.setVisible(False)
        self.textEdit_5.setVisible(False)
        self.scrollArea.setVisible(False)
        self.scrollAreaWidgetContents.setVisible(False)

    def hide4(self):
        self.label_11.setVisible(False)
        self.progressBar.setVisible(False)
        self.show_sArea()
        # 讨论区
        # 4
        self.pushButton_15.setVisible(True)
        self.textEdit_5.setVisible(True)
        self.scrollArea.setVisible(True)
        self.scrollAreaWidgetContents.setVisible(True)

        # 1
        self.pushButton.setVisible(False)
        self.lineEdit.setVisible(False)
        self.label_16.setVisible(False)
        self.label_17.setVisible(False)
        self.label_18.setVisible(False)
        self.lineEdit_1.setVisible(False)
        self.textEdit.setVisible(False)
        self.pushButton_12.setVisible(False)
        self.pushButton_13.setVisible(False)

        # 2
        self.label.setVisible(False)
        self.textEdit_2.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.label_11.setVisible(False)
        self.label_13.setVisible(False)
        self.label_14.setVisible(False)
        self.label_15.setVisible(False)
        self.progressBar.setVisible(False)
        self.pushButton_6.setVisible(False)
        self.pushButton_7.setVisible(False)
        self.pushButton_8.setVisible(False)
        self.pushButton_9.setVisible(False)
        self.pushButton_11.setVisible(False)
        self.combox.setVisible(False)
        self.spinbox_1.setVisible(False)
        self.spinbox_2.setVisible(False)
        self.hSlider_1.setVisible(False)
        self.hSlider_2.setVisible(False)

        #3
        self.tableView.setVisible(False)
        self.lb1.setVisible(False)
        self.lb2.setVisible(False)
        self.lb3.setVisible(False)
        self.lb4.setVisible(False)
        self.lb5.setVisible(False)
        self.lb6.setVisible(False)
        self.mail.setVisible(False)
        self.LEdit.setVisible(False)
        self.rdio.setVisible(False)
        self.rdio1.setVisible(False)
        self.dEdit.setVisible(False)
        self.pBtn.setVisible(False)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    all = main()
    all.show()
    sys.exit(app.exec_())