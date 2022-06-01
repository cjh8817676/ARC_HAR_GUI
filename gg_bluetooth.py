# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import*
import numpy as np
import threading
import pandas as pd
from matplotlib import pyplot as plt
from pyqtgraph.Qt import QtGui, QtCore
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import model
import serial
import os, sys
import random
import pyqtgraph as pg


model = model.HalNet()
model.build((None,50,3,1))
model.compile(loss='categorical_crossentropy', optimizer="Adam", metrics=['accuracy'])
model.load_weights('./one_input_gru/one_input_gru')


start_flag = 0
activity = 'Walking'
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1053, 636)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(760, 0, 111, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(190, 0, 131, 21))
        self.label_2.setObjectName("label_2")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 380, 471, 202))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton_3 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout.addWidget(self.radioButton_3, 2, 0, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 2, 2, 1)

        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 2, 2, 1)

        self.radioButton_5 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout.addWidget(self.radioButton_5, 4, 0, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 1, 0, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout.addWidget(self.radioButton_4, 3, 0, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout.addWidget(self.radioButton_6, 5, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 1, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 5, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 2, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(650, 510, 321, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 1, 1, 1)



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "ARC SENSOR:"))
        self.label_2.setText(_translate("Form", "Train Dataset"))
        self.radioButton_3.setText(_translate("Form", "Upstairs"))
        self.pushButton_3.setText(_translate("Form", "Graph"))
        self.pushButton_4.setText(_translate("Form", "Check"))
        self.radioButton_5.setText(_translate("Form", "Sitting"))
        self.radioButton_2.setText(_translate("Form", "Walking"))
        self.radioButton_4.setText(_translate("Form", "Downstairs"))
        self.radioButton_6.setText(_translate("Form", "Standing"))
        self.label_3.setText(_translate("Form", "User No."))
        self.radioButton.setText(_translate("Form", "Jogging"))
        self.pushButton_2.setText(_translate("Form", "Start"))
        self.pushButton.setText(_translate("Form", "Finish"))

class AppWindow(QDialog): 
    def __init__(self):
        super().__init__()
        self.activity = 'Walking'
        
        self.ui = Ui_Form() #新增剛剛拉的前端介面
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.receive_finish)
        self.ui.pushButton_2.clicked.connect(self.receive_start)
        self.ui.pushButton_3.clicked.connect(self.plot_data)
        self.ui.pushButton_4.clicked.connect(self.plot_act)
        self.ui.radioButton.toggled.connect(self.onClicked)
        self.ui.radioButton_2.toggled.connect(self.onClicked)
        self.ui.radioButton_3.toggled.connect(self.onClicked)
        self.ui.radioButton_4.toggled.connect(self.onClicked)
        self.ui.radioButton_5.toggled.connect(self.onClicked)
        self.ui.radioButton_6.toggled.connect(self.onClicked)
        
        self.user_number = self.ui.textEdit.toPlainText()
        self.chart = Canvas(self)
        self.chart.move(20,60)
        
        self.chart2 = Canvas2()
        self.chart2.move(550,70)

        self.show() #沒有這行run的時候就不會show了

    def onClicked(self):
        radioBtn = self.sender()
        #print(type(self.ui.textEdit.toPlainText()))
        if radioBtn.isChecked():
            print(radioBtn.text())
            self.activity = radioBtn.text()
            self.ui.textBrowser


    def receive_start(self):
        self.chart2.receive_data()
    def receive_finish(self):
        pass
    def plot_data(self):
        #print(self.chart)
        self.chart.plot(int(self.ui.textEdit.toPlainText()),self.activity)
    def plot_act(self):
        self.ui.textBrowser.clear()
        acts = self.chart.list_action(int(self.ui.textEdit.toPlainText()))
        str = ""
        for act in acts:
            str += act
        self.ui.textBrowser.setText(str)
        
class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.fig = Figure(figsize=(5, 3), dpi=100)
        super(FigureCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.data = []
        self.setParent(parent)
        self.df =  self.get_data_pd()
        
        #self.data = self.get_data_numpy(self.df)
      
    def get_data_pd(self):
        columns = ['user','activity','timestamp', 'x-axis', 'y-axis', 'z-axis']
        df = pd.read_csv('./dataset/WISDM_ar_v1.1_raw.txt', header = None, names = columns, on_bad_lines='skip')
        df_har = df.dropna()
        # transforming the z-axis to float
        df_har['z-axis'] = df_har['z-axis'].str.replace(';', '')
        df_har['z-axis'] = df_har['z-axis'].apply(lambda x:float(x))
        # drop rows where timestamp is 0
        df = df_har[df_har['timestamp'] != 0]
        # arrange data in ascending order of user and timestamp

        return df

    def get_data_numpy(self,df):
        df_data = []
        for ind in df.columns:
            if ind == 'x-axis' or ind == 'y-axis' or ind == 'z-axis':
                df_data.append(df[ind])
        
        df_data = np.array(df_data)
        return df_data

    def plot(self, user=36, activity='Walking'):
        len = 50
        self.ax.clear()
        self.ax.grid()
        num = random.randint(1,100)
        data_user = self.df[(self.df['user'] == user) & (self.df['activity'] == activity)][num:num+len]
        data = self.get_data_numpy(data_user)
        t = np.arange(0.0, len * 0.05 , 0.05)
        self.ax.plot(t, data[0][0:len],label='x')
        self.ax.plot(t, data[1][0:len],label='y')
        self.ax.plot(t, data[2][0:len],label='z')
        self.ax.legend()
        print('plot here')
        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
               title= str(user) +' ' +activity)
        self.fig.canvas.draw_idle()   # 這個記得要加，不然畫完瞬間被刷新 呵呵。
        
        # 在官方文档中的描述是用于重画图表，因此尝试使用，最终解决了问题
    def list_action(self,user = 36):
        dff = self.df[self.df["user"] == user]["activity"]
        act = []
        for i in dff.drop_duplicates():
            act.append(i)
        return act

class Canvas2(QtGui.QWidget,threading.Thread):  # 畫布二 自行成一個執行續。
    def __init__(self):
        self.bserial = serial.Serial(port='COM7', baudrate=38400, timeout=0, parity=serial.PARITY_NONE, stopbits=1)
        self.label_class = ['stairs','Jogging','Sitting','Standing','stairs','Walking']
        self.l1 = []
        self.l2 = []
        self.l3 = []
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.p1= self.win.addPlot()
        self.curve1 = self.p1.plot(self.l1,pen=pg.mkPen('r', width=1))
        self.curve2 = self.p1.plot(self.l2,pen=pg.mkPen('g', width=1))
        self.curve3 = self.p1.plot(self.l3,pen=pg.mkPen('b', width=1))
        ptr1 = 0
        self.t = threading.Thread(target = self.blue_receive)
        #self.t2 = threading.Thread(target = self.update1)
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update1)
        self.timer.start(50)


    def blue_receive(self):
        while (1):
            a = b''
            endLine = False
            if flag == False:
                self.bserial.write(b'egg')   #hc-05
                self.bserial.write(b"\r\n")  #hc-05
                flag = True
            else:
                while(1):
                    c = self.bserial.read() # 1ms  hc-05
                    #c = self.connection.rx_data  
                    #print(c)
                    count += 1
                    if(c != b''):
                        #print(c)
                        count = 0
                        if(c == b'\xff' and endLine == False):
                            endLine = True
                        elif (c == b'\xff' and endLine == True):
                            break
                        elif endLine == True:
                            a += b'\xff'
                            a += c
                            endLine = False
                        else:
                            a += c
                            endLine = False 
                if( len(a) == 15):
                    x = a[4] + (a[6] << 8 | a[5]) * 0.001
                    y = a[8] + (a[10] << 8 | a[9]) * 0.001
                    z = a[12] + (a[14] << 8 | a[13]) * 0.001  
                    print("data:{} X:{}{} Y:{}{} Z:{}{}".format(
                        (a[1] << 8 | a[2]),
                        '+' if a[3] else '-', 
                        x,
                        '+' if a[7] else '-', 
                        y,
                        '+' if a[11] else '-', 
                        z
                        )   
                    )
                    #print(s)
                    if a[3] == 0:
                        x = -1*x
                    if a[7] == 0:
                        y = -1*y
                    if a[11] == 0:
                        z = -1*z    
                    self.l1.append(x)
                    self.l2.append(z)
                    self.l3.append(y)  

    def update1(self):
        label_class = ['Stairs','Jogging','Sitting','Walking','Stairs','Walking','Standing','Sitting']
        try:
            pg.plotWidget_ted.setTitle( label_class[int(predict.hex())] )
        except:
            pass

        self.l1[:-1] = self.l1[1:]
        self.l2[:-1] = self.l2[1:]
        self.l3[:-1] = self.l3[1:]

        while(self.l1.__len__() > 300):
            #print(len(self.l1))
            self.l1.pop(0)
            self.l2.pop(0)
            self.l3.pop(0)
        # 数据填充到绘制曲线中
        curve1.setData(l1)
        curve2.setData(l2)
        curve3.setData(l3)

                    
    def receive_data(self):  
        # Create the event loop.
        self.t.start()
        QtGui.QApplication.instance().exec_()
        self.t.join()

    def close_bluetooth(self):
        #self.serial.close()
        pass


if __name__ == '__main__':
    # from multiprocessing import Process
    app = QApplication(sys.argv)
    
    w = AppWindow()
    w.show()
    #serialPort.close()
    sys.exit(app.exec_())
