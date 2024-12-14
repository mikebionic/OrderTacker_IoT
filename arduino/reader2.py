
import serial # from https://pyserial.readthedocs.io
import time

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

while True:
    echoLine = ser.readline()
    print(echoLine);
    print(); # empty line
