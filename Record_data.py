# import pyqtgraph.examples
# pyqtgraph.examples.run()

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the speed of rapidly updating multiple plot curves
"""
from datetime import datetime
import serial
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from time import perf_counter
from threading import Thread, Event
import time # 引入time
# import model
bserial = serial.Serial(port='COM7', baudrate=38400, timeout=0, parity=serial.PARITY_NONE, stopbits=1)
l1 = []
l2 = []
l3 = []
predict = b'\x00'
user = "18"
action ="Walking"
path = './'+action+".txt"
f = open(path, 'w')    

# Harnet = model.HalNet()
# Harnet.build((None,50,3,1))
# Harnet.compile(loss='categorical_crossentropy', optimizer="Adam", metrics=['accuracy'])
# Harnet.load_weights('./one_input_gru/one_input_gru')

def blue_receive():
    global predict
    global l1 
    global l2
    global l3
    count = 0
    temp = True
    flag = False
    '''READER LOOP'''
    print('start to read')
    while (1):
        a = b''
        endLine = False
        if flag == False:
            bserial.write(b'egg')   #hc-05
            bserial.write(b"\r\n")  #hc-05
            flag = True
        else:
            while(1):
                c = bserial.read() # 1ms  hc-05
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
                now = datetime.now()
                s = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
                timeString = s # 時間格式為字串
                struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
                time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
                f.write(user+","+action+","+str(time_stamp)+",{}{},{}{},{}{}\n".format('+' if a[3] else '-', x,'+' if a[7] else '-', y,'+' if a[11] else '-', z))
                print(s)
                if a[3] == 0:
                    x = -1*x
                if a[7] == 0:
                    y = -1*y 
                if a[11] == 0:
                    z = -1*z    
                l1.append(x)
                l2.append(z)
                l3.append(y)  
                #serialPort.write(b"\r\n")
            if ((a[1] <<8 | a[2]) >= 300):
                predict = bserial.read() # 1ms
                print('predict',predict)
                #preditct = Harnet.predict()
# label_class = ['Stairs','Jogging','Sitting','Walking','Stairs','Walking','Standing','Sitting']

win = pg.GraphicsLayoutWidget(show=True)
# win.setWindowTitle(label_class[int(predict.hex())])
p1= win.addPlot()

curve1 = p1.plot(l1,pen=pg.mkPen('r', width=1))
curve2 = p1.plot(l2,pen=pg.mkPen('g', width=1))
curve3 = p1.plot(l3,pen=pg.mkPen('b', width=1))
ptr1 = 0
'''
l1 = [1,2,3,4,5,6,7,8,9,10]
l1[:-1] => [1,2,3,4,5,6,7,8,9]
l1[:1] => [1] 
'''
def update1():
    global ptr1, l1,l2,l3, predict

    l1[:-1] = l1[1:]
    l2[:-1] = l2[1:]
    l3[:-1] = l3[1:]

    while(l1.__len__() > 300):
        #print(len(self.l1))
        l1.pop(0)
        l2.pop(0)
        l3.pop(0)
    # 数据填充到绘制曲线中
    curve1.setData(l1)
    curve2.setData(l2)
    curve3.setData(l3)

timer = pg.QtCore.QTimer()
timer.timeout.connect(update1)
timer.start(50)

if __name__ == '__main__':
    import sys
    t = Thread(target=blue_receive)
    t.start()
    QtGui.QApplication.instance().exec_()
    t.join()
