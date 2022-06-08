# import pyqtgraph.examples
# pyqtgraph.examples.run()

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the speed of rapidly updating multiple plot curves
"""

import serial
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import PlotWidget
import numpy as np
import pyqtgraph as pg
from time import perf_counter
import threading
import pyqtgraph as pq




class Window(QtGui.QWidget,threading.Thread):
    def __init__(self):
        super().__init__()
        super(threading.Thread, self).__init__()
        # 设置下尺寸
        #self.resize(800,800)
        # 添加 PlotWidget 控件
        self.plotWidget_ted = PlotWidget(self)
        # 设置该控件尺寸和相对位置
        self.plotWidget_ted.setGeometry(QtCore.QRect(0,0,800,500))
        self.plotWidget_ted.addLegend()
        self.label_class = ['Jogging','Sitting','Standing','Walking']

        # 设定定时器
        self.timer = pq.QtCore.QTimer()
        # 定时器信号绑定 update_data 函数
        self.timer.timeout.connect(self.update_data)
        # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
        self.timer.start(50)
        self.act = 0
        self.bserial = serial.Serial(port='COM5', baudrate=38400, timeout=0, parity=serial.PARITY_NONE, stopbits=1)
        self.l1 = []
        self.l2 = []
        self.l3 = []

        self.t = threading.Thread(target= self.blue_receive)
        self.t.start()
        self.curve1 = self.plotWidget_ted.plot(self.l1, name="x",pen=pg.mkPen('r', width=1))
        self.curve2 = self.plotWidget_ted.plot(self.l2, name="y",pen=pg.mkPen('g', width=1))
        self.curve3 = self.plotWidget_ted.plot(self.l3, name="z",pen=pg.mkPen('b', width=1))
        self.ptr1 = 0
        
    def update_data(self):
        try:
            self.plotWidget_ted.setTitle( self.label_class[int(self.act.hex())] )
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
        self.curve1.setData(self.l1)
        self.curve2.setData(self.l2)
        self.curve3.setData(self.l3)

        # x 轴记录点
        # self.ptr1 += 1 / 120
        # self.ptr1 = 0
        # # 重新设定 x 相关的坐标原点
        # self.curve1.setPos(self.ptr1,0)
        # self.curve2.setPos(self.ptr1,0)
        # self.curve3.setPos(self.ptr1,0)


    def blue_receive(self):
        count = 0
        temp = True
        flag = False
        '''READER LOOP'''
        print('start to read')
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
                    print(c)
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
                    # elif(count > 1000 * 10):
                    #     print('time_up')
                    #     temp = False
                    #     break
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
                    #serialPort.write(b"\r\n")
                if ((a[1] <<8 | a[2]) == 128):
                    while(1):
                        predict = self.bserial.read() # 1ms
                        if predict != b'':
                            self.act = predict
                            print(self.act)
                            break
            # if temp ==False:
            #     print('time_up2')
            #     break



if __name__ == '__main__':
    import sys
    # PyQt5 程序固定写法
    app = QtGui.QApplication(sys.argv)

    # 将绑定了绘图控件的窗口实例化并展示
    window = Window()
    window.show()

    # PyQt5 程序固定写法
    sys.exit(app.exec())
