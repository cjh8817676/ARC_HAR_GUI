import serial


s = serial.Serial(port='COM5',
                  baudrate=38400,
                  timeout=0,
                  parity=serial.PARITY_NONE,
                  stopbits=1)
s.write(b'egg')   #hc-05
s.write(b"\r\n")  #hc-05

window = b''
while True:
    c = s.read()
    if c == b'':
        continue
    window += c
    if len(window) > 17:
        window = window[1:]

    print(window)