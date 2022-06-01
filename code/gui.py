import serial
from display import App
from threading import Thread, Event

s = serial.Serial(port='COM7',
                  baudrate=38400,
                  timeout=0,
                  parity=serial.PARITY_NONE,
                  stopbits=1)

s.write(b'egg')   #hc-05
s.write(b"\r\n")  #hc-05

app = App()

window = b''
while True:
    c = s.read()
    if c == b'':
        continue
    window += c
    if len(window) > 17:
        window = window[1:]

    if len(window) == 17 and window[15] == 255 and window[16] == 255:

        number_of_data = window[1] << 8 | window[2]
        if number_of_data > 300:
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
        
        app.update(x,y,z)
        # print("data:{:3} X:{:+4f} Y:{:+4f} Z:{:+4f}".format(
        #     number_of_data, x, y, z))
        # print(f"data:{number_of_data:3} X:{x:+.3f} Y:{y:+.3f} Z:{z:+.3f}")

        # if number_of_data == 300:
        #     while True:
        #         c = s.read()
        #         if c != b'':
        #             print(" " * 45, "Model predict :", c)
        #             break
