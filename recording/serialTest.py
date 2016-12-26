import serial
import struct
import time
global srl
srl= serial.Serial('/dev/ttyACM1', 19200)
time.sleep(3)
def callback():
#    global srl
    srl.write(struct.pack('cBB', "r", 6, 100))
    srl.write(struct.pack('cBB', "r", 7, 150))
    srl.write(struct.pack('cBB', "r", 8, 190))
    srl.write(struct.pack('cBB', "r", 9, 100))


x=1
if x:
    callback()
srl.close()