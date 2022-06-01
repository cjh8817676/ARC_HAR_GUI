import tkinter
import numpy as np
import time


class App():
    def __init__(self):
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 720
        # self.window = self.create_window()
        # self.canvas = self.create_canvas(self.window)
        self.create_window()
        self.create_canvas()
        self.x = []
        self.y = []
        self.z = []

    def create_window(self):
        self.window = tkinter.Tk()
        self.window.title("GUI title")
        # Uses python 3.6+ string interpolation
        self.window.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')

    def create_canvas(self):
        self.canvas = tkinter.Canvas(self.window)
        # canvas.configure(bg="white")
        self.canvas.pack(fill="both", expand=True)
        # canvas.pack()

    def update(self, x,y,z):
        x = (x+4)*50
        y = (y+4)*50
        z = (z+4)*50
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        if len(self.x) > 300:
            self.x = self.x[1:]
            self.y = self.y[1:]
            self.z = self.z[1:]
        # print(self.data)
        self.canvas.delete('all')
        for i in range(1,len(self.x)):
            self.canvas.create_line((i-1)*2,self.x[i-1],i*2,self.x[i])
            self.canvas.create_line((i-1)*2,self.y[i-1],i*2,self.y[i])
            self.canvas.create_line((i-1)*2,self.z[i-1],i*2,self.z[i])
        self.window.update()

    
    # while True:
    #     new_val = (1-np.random.random())*4*100
    #     data[:-1] = data[1:]
    #     data[-1] = new_val
    #     update(window, canvas, data)
    #     time.sleep(0.01)
    #     window.update()