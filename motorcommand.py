import serial
from random import *
import time
ser = serial.Serial(
    port='/dev/ttyACM1',
    baudrate=115200
)

ser.isOpen()

def send_command(m,val):
    ser.write(str(m)+':'+str(val)+';')

y=0

while(1):
    send_command(1,90)
    print '90'
    time.sleep(3)
    send_command(1, -90)
    print '-90'
    time.sleep(3)


