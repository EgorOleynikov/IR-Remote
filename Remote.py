from curses import baudrate
import serial
ser = serial.Serial(port="COM5", baudrate=9600)  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'hello')     # write a string
ser.close()             # close port