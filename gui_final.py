import tkinter as tk
import numpy as np
import serial
from threading import Thread
import _tkinter


model_predict = b''
step_count = 0
WINDOW_WIDTH = 680
WINDOW_HEIGHT = 580

initial_val = WINDOW_HEIGHT-4*50
x_datas = [initial_val]*128
y_datas = [initial_val]*128
z_datas = [initial_val]*128
label_class = ['Jogging','Sitting','Standing','Walking']
def blue(stop):
    s = serial.Serial(port='COM5',
                  baudrate=38400,
                  timeout=0,
                  parity=serial.PARITY_NONE,
                  stopbits=1)
    global x_datas,y_datas,z_datas,model_predict,step_count
    s.write(b'egg')   #hc-05
    s.write(b"\r\n")  #hc-05
    window = b''
    while True:
        if stop():
            break
        c = s.read()
        if c == b'':
            continue
        window += c
        if len(window) > 17:
            window = window[1:]

        if len(window) == 17 and window[15] == 255 and window[16] == 255:

            number_of_data = window[1] << 8 | window[2]
            if number_of_data > 128:
                # illegal data ( when frac_part == 0xffff )
                continue
            x = window[4] + (window[6] << 8 | window[5]) * 0.001
            y = window[8] + (window[10] << 8 | window[9]) * 0.001
            z = window[12] + (window[14] << 8 | window[13]) * 0.001
            if window[3] == False:
                x = -x
            if window[7] == False:
                y = -y
            if window[11] == False:
                z = -z
            
            print(f"data:{number_of_data:3} X:{x:+.3f} Y:{y:+.3f} Z:{z:+.3f}")
            x_datas.append(WINDOW_HEIGHT-(x+4)*50)
            y_datas.append(WINDOW_HEIGHT-(y+4)*50)
            z_datas.append(WINDOW_HEIGHT-(z+4)*50)
            x_datas = x_datas[1:]
            y_datas = y_datas[1:]
            z_datas = z_datas[1:]
            
            if number_of_data == 128:
                while True:
                    c = s.read()
                    if c != b'':
                        print(" " * 45, "Model predict :", c)
                        # model_predict = c
                        model_predict = label_class[int(c.hex())]
                        
                        # TODO: add step count data
                        step_count += 1
                        break

class App():
    def __init__(self):
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.create_window()
        self.create_canvas()

    def create_window(self):
        self.window = tk.Tk()
        self.window.title("防誤判計步器")
        self.window.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window)
        self.canvas.configure(background="white")
        self.canvas.pack(fill="both", expand=True)

    
    def update(self):
        global x_datas,y_datas,z_datas,model_predict,step_count
        self.canvas.delete('all')
        scale = 2
        offset = 40
        FONT = "Calibri"
        self.canvas.create_text(offset,offset,text=f"X Accelerometer", font=(FONT, 16),anchor=tk.NW, fill='red')
        self.canvas.create_text(offset,offset+30,text=f"Y Accelerometer", font=(FONT, 16),anchor=tk.NW, fill='green')
        self.canvas.create_text(offset,offset+60,text=f"Z Accelerometer", font=(FONT, 16),anchor=tk.NW, fill='blue')
        
        H_CENTER = WINDOW_WIDTH//2
        self.canvas.create_text(H_CENTER,offset+15,text=f"Model predict:{model_predict}", font=(FONT, 16),anchor=tk.NW)
        self.canvas.create_text(H_CENTER,offset+45,text=f"Step Count   :{step_count}", font=(FONT, 16),anchor=tk.NW)
        
        FIG_LEFT = WINDOW_WIDTH-offset-600
        FIG_RIGHT = WINDOW_WIDTH-offset
        self.canvas.create_rectangle(FIG_LEFT,WINDOW_HEIGHT-offset-400,FIG_RIGHT,WINDOW_HEIGHT-offset)
        self.canvas.create_line(FIG_LEFT,WINDOW_HEIGHT-offset-100,FIG_RIGHT,WINDOW_HEIGHT-offset-100, dash=(2, 8))
        self.canvas.create_line(FIG_LEFT,WINDOW_HEIGHT-offset-200,FIG_RIGHT,WINDOW_HEIGHT-offset-200, dash=(2, 8))
        self.canvas.create_line(FIG_LEFT,WINDOW_HEIGHT-offset-300,FIG_RIGHT,WINDOW_HEIGHT-offset-300, dash=(2, 8))
        
        self.canvas.create_text(offset,WINDOW_HEIGHT-offset,text=f"-2", font=(FONT, 12),anchor=tk.E)
        self.canvas.create_text(offset,WINDOW_HEIGHT-offset-100,text=f"-1", font=(FONT, 12),anchor=tk.E)
        self.canvas.create_text(offset,WINDOW_HEIGHT-offset-200,text=f" 0", font=(FONT, 12),anchor=tk.E)
        self.canvas.create_text(offset,WINDOW_HEIGHT-offset-300,text=f" 1", font=(FONT, 12),anchor=tk.E)
        self.canvas.create_text(offset,WINDOW_HEIGHT-offset-400,text=f" 2", font=(FONT, 12),anchor=tk.E)
        for i in range(1, 128):
            nowX = offset+(i - 1) * scale
            prevX = offset+i * scale
            self.canvas.create_line(nowX, x_datas[i - 1]-offset, prevX,
                                    x_datas[i]-offset, fill='red')
            self.canvas.create_line(nowX, y_datas[i - 1]-offset, prevX,
                                    y_datas[i]-offset, fill='green')
            self.canvas.create_line(nowX, z_datas[i - 1]-offset, prevX,
                                    z_datas[i]-offset, fill='blue')
        self.window.update()


if __name__ == "__main__":
    stop_threads = False
    t = Thread(target=blue, args =(lambda : stop_threads, ))
    t.start()
    app = App()
    while True:
        try:
            app.update()
        except KeyboardInterrupt:
            print("KeyboardInterrupt, close program.")
            stop_threads = True
            break
        except _tkinter.TclError:
            print("TclError, close program.")
            stop_threads = True
            break
    t.join()