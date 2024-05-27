import time
import serial

port_read = '/dev/ttyACM2'  # Specify the correct serial port name

baud_rate = 115200  # Specify the baud rate

ser_read = serial.Serial(port_read, baud_rate)

try:
    print("Reading data stream...")
    while True:
        if ser_read.in_waiting == 0:
            continue
        data = ser_read.read(ser_read.in_waiting)
        print(data)

except KeyboardInterrupt:
    ser_read.close()
    print('Serial port is closed')
except Exception as e:
    print(f"Error: {e}")
