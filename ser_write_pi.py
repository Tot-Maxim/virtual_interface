#!/usr/bin/env python3
import serial
import time

port_write = '/dev/ttyACM0'

baud_rate = 115200  # Specify the baud rate

ser_wrtie = serial.Serial(port_write, baud_rate)

data_to_send = b''

for i in range(3):
    data_to_send += bytes([i])

try:
    while True:
        data = ser_wrtie.write(data_to_send)
        print(f'Write {data_to_send} to {port_write}')
        time.sleep(0.2)

except KeyboardInterrupt:
    ser_wrtie.close()
    print('Serial port is closed')
except Exception as e:
    print(f"Error: {e}")
