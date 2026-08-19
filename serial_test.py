import time
import serial

sld = serial.Serial('COM3', 115200)

sld.write(b'id?\r')
time.sleep(1)
print(sld.read(sld.in_waiting))

sld.close()
