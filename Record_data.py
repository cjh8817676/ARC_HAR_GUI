# import pyqtgraph.examples
# pyqtgraph.examples.run()

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Test the speed of rapidly updating multiple plot curves
"""
import serial

import numpy as np
import pyqtgraph as pg
from time import perf_counter
import threading
import time # 引入time
from datetime import datetime
from PyQt5 import Qt
user = "18"
action ="Walking"
path = './'+action+".txt"
f = open(path, 'w')    


# model = model.HalNet()
# model.build((None,50,3,1))
# model.compile(loss='categorical_crossentropy', optimizer="Adam", metrics=['accuracy'])
# model.load_weights('./one_input_gru/one_input_gru')


def blue_receive(bserial):
    counter =0 
    count = 0
    temp = True
    flag = False
    x = input()
    print('start to read')
    result = []
    while (x):
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
                # print(c)
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
                    counter,
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
                # f.write(user+","+action+","+str(time_stamp)+","+str(x)+","+str(y)+","+str(z)+"\n")
                counter+=1
                print(counter)
                if counter == 119*60*3: #錄製3分鐘
                    f.close()
                    break
                #print(s)
                if a[3] == 0:
                    x = -1*x
                if a[7] == 0:
                    y = -1*y
                if a[11] == 0:
                    z = -1*z  
                result.append([x,y,z])   
            if (len(result) == 300):
                new_data = []
                for i in range(0,len(result),6):  
                    new_data.append(result[i])
                new_data = np.array(new_data)

                
                
                

if __name__ == '__main__':
    b_serial = serial.Serial(port='COM7', baudrate=38400, timeout=0, parity=serial.PARITY_NONE, stopbits=1)
    blue_receive(b_serial)
